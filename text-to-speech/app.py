
from io import BytesIO
import subprocess
import os
import re
import unicodedata

from flask import (
    Flask,
    request,
    jsonify,
    send_file,
    render_template_string
)

from gtts import gTTS
import imageio_ffmpeg


app = Flask(__name__)

# =========================
# FFMPEG CONFIG
# =========================

FFMPEG_PATH = imageio_ffmpeg.get_ffmpeg_exe()

print("========== CHECK FFMPEG ==========")
print("FFmpeg:", FFMPEG_PATH)
print("Exists:", os.path.isfile(FFMPEG_PATH))
print("=================================")


# =========================
# VIETNAMESE SPELLING
# =========================

ONSETS = {
    "ngh": "ngờ",
    "ng": "ngờ",
    "nh": "nhờ",
    "kh": "khờ",
    "ph": "phờ",
    "th": "thờ",
    "tr": "trờ",
    "ch": "chờ",
    "gh": "gờ",
    "gi": "giờ",
    "qu": "quờ",

    "b": "bờ",
    "c": "cờ",
    "d": "dờ",
    "đ": "đờ",
    "g": "gờ",
    "h": "hờ",
    "k": "cờ",
    "l": "lờ",
    "m": "mờ",
    "n": "nờ",
    "p": "pờ",
    "r": "rờ",
    "s": "sờ",
    "t": "tờ",
    "v": "vờ",
    "x": "xờ",
}

CODAS = {
    "ch": "chờ",
    "ng": "ngờ",
    "nh": "nhờ",
    "c": "cờ",
    "m": "mờ",
    "n": "nờ",
    "p": "pờ",
    "t": "tờ",
}

VOWELS = {
    "a": "a",
    "ă": "ă",
    "â": "â",
    "e": "e",
    "ê": "ê",
    "i": "i",
    "o": "o",
    "ô": "ô",
    "ơ": "ơ",
    "u": "u",
    "ư": "ư",
    "y": "i",
}

VOWEL_COMBINATIONS = [
    "ươu", "iêu", "yêu", "uôi", "ươi",
    "uya", "uyê", "uây", "oai", "oay",
    "oeo", "oao", "iê", "yê", "uô",
    "ươ", "oa", "oe", "uy", "ai", "ao",
    "au", "ay", "âu", "ây", "eo", "êu",
    "ia", "iu", "oi", "ôi", "ơi", "ua",
    "uâ", "ưa", "ưi", "ưu", "ui",
]

TONE_NAMES = {
    "sắc": "sắc",
    "huyền": "huyền",
    "hỏi": "hỏi",
    "ngã": "ngã",
    "nặng": "nặng",
    "ngang": "",
}


def remove_tone(text):
    """Bỏ dấu thanh, giữ nguyên dấu mũ, râu, trăng."""

    tone_marks = {
        "\u0300",  # huyền
        "\u0301",  # sắc
        "\u0303",  # ngã
        "\u0309",  # hỏi
        "\u0323",  # nặng
    }

    result = []

    for char in unicodedata.normalize("NFD", text):
        if char not in tone_marks:
            result.append(char)

    return unicodedata.normalize("NFC", "".join(result))


def get_tone(word):
    """Xác định thanh điệu."""

    normalized = unicodedata.normalize("NFD", word)

    if "\u0301" in normalized:
        return "sắc"

    if "\u0300" in normalized:
        return "huyền"

    if "\u0309" in normalized:
        return "hỏi"

    if "\u0303" in normalized:
        return "ngã"

    if "\u0323" in normalized:
        return "nặng"

    return "ngang"


def split_vietnamese_syllable(word):
    """Tách phụ âm đầu, nguyên âm và phụ âm cuối."""

    word = word.lower()
    plain_word = remove_tone(word)

    onset = ""

    # Tách phụ âm đầu, ưu tiên tổ hợp dài nhất
    for item in sorted(ONSETS.keys(), key=len, reverse=True):
        if plain_word.startswith(item):
            onset = item
            break

    remaining = plain_word[len(onset):]

    coda = ""

    # Tách phụ âm cuối
    for item in sorted(CODAS.keys(), key=len, reverse=True):
        if remaining.endswith(item) and len(remaining) > len(item):
            coda = item
            break

    vowel = remaining[:-len(coda)] if coda else remaining

    if not vowel:
        return None

    return onset, vowel, coda


def spell_vowel(vowel):
    """Đọc thành phần nguyên âm."""

    if len(vowel) == 1:
        return [VOWELS.get(vowel, vowel)]

    parts = []

    for char in vowel:
        parts.append(VOWELS.get(char, char))

    parts.append(vowel)

    return parts


def spell_word(word):
    """Tạo chuỗi hướng dẫn đánh vần một tiếng."""

    parsed = split_vietnamese_syllable(word)

    if not parsed:
        return word

    onset, vowel, coda = parsed

    steps = []

    # 1. Phụ âm đầu
    if onset:
        steps.append(ONSETS.get(onset, onset))

    # 2. Nguyên âm
    steps.extend(spell_vowel(vowel))

    # 3. Phụ âm cuối và vần
    if coda:
        coda_sound = CODAS.get(coda)

        if coda_sound:
            steps.append(coda_sound)

        steps.append(vowel + coda)

    # 4. Ghép tiếng chưa có thanh
    base_word = remove_tone(word)

    if onset:
        steps.append(base_word)

    # 5. Thanh điệu và tiếng hoàn chỉnh
    tone = get_tone(word)

    if tone != "ngang":
        steps.append(TONE_NAMES[tone])
        steps.append(word)

    return " ".join(steps)


def process_spelling(text, spell):

    if spell == "normal":
        return text

    if spell == "spell":

        words = re.findall(
            r"[^\W\d_]+|[^\w\s]",
            text,
            flags=re.UNICODE
        )

        result = []

        for word in words:

            if re.fullmatch(
                r"[^\W\d_]+",
                word,
                flags=re.UNICODE
            ):
                result.append(spell_word(word))
            else:
                result.append(word)

        # Phần 1: Đánh vần toàn bộ văn bản
        spelling_text = " ... ".join(result)

        # Phần 2: Đọc lại nguyên văn câu ban đầu
        final_text = text

        # Kết hợp hai phần
        return spelling_text + " ... " + final_text

    return text

# =========================
# HTML INTERFACE
# =========================

HTML = """
<!DOCTYPE html>
<html lang="vi">

<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <title>Vietnamese Text to Speech</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            padding: 40px 16px;
            background: #f4f6f9;
            font-family: Arial, sans-serif;
            color: #222;
        }

        .container {
            max-width: 700px;
            margin: auto;
            padding: 28px;
            background: white;
            border-radius: 14px;
            box-shadow: 0 4px 20px #0000000d;
        }

        h2 {
            margin-top: 0;
        }

        textarea {
            width: 100%;
            min-height: 170px;
            padding: 14px;
            border: 1px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            resize: vertical;
        }

        label {
            display: block;
            margin-top: 18px;
            margin-bottom: 8px;
            font-weight: bold;
        }

        select, button {
            padding: 12px;
            border-radius: 8px;
            font-size: 15px;
        }

        select {
            width: 100%;
            margin-bottom: 10px;
            border: 1px solid #ddd;
            background: white;
        }

        button {
            width: 100%;
            margin-top: 12px;
            border: none;
            background: #2563eb;
            color: white;
            cursor: pointer;
        }

        button:disabled {
            opacity: .6;
            cursor: wait;
        }

        audio {
            width: 100%;
            margin-top: 20px;
        }

        #download {
            display: none;
            margin-top: 14px;
            color: #2563eb;
            text-decoration: none;
        }

        #status {
            margin-top: 14px;
            color: #555;
        }

        .note {
            font-size: 13px;
            color: #777;
            margin-top: 16px;
        }
    </style>
</head>

<body>

<div class="container">

    <h2>Vietnamese Text to Speech</h2>

    <p>
        Nhập văn bản tiếng Việt để chuyển thành giọng nói.
    </p>

    <label>Nội dung văn bản</label>

    <textarea
        id="text"
        placeholder="Nhập nội dung cần đọc..."
    ></textarea>

    <label>Chế độ đọc</label>

    <select id="spell">
        <option value="normal">
            Không đánh vần
        </option>

        <option value="spell">
            Đánh vần tiếng Việt
        </option>
    </select>

    <label>Tốc độ đọc</label>

    <select id="speed">
        <option value="normal">
            Tốc độ bình thường
        </option>

        <option value="slow">
            Đọc chậm
        </option>
    </select>

    <button id="generate" onclick="generateAudio()">
        Tạo giọng đọc
    </button>

    <p id="status"></p>

    <audio id="audio" controls style="display:none"></audio>

    <a id="download" download="speech.wav">
        Tải file WAV
    </a>

    <p class="note">
        Sử dụng Google TTS (gTTS).
        Cần kết nối Internet.
    </p>

</div>

<script>

async function generateAudio() {

    const text = document.getElementById("text").value.trim();
    const speed = document.getElementById("speed").value;
    const spell = document.getElementById("spell").value;

    const button = document.getElementById("generate");
    const status = document.getElementById("status");
    const audio = document.getElementById("audio");
    const download = document.getElementById("download");

    if (!text) {
        alert("Vui lòng nhập nội dung!");
        return;
    }

    button.disabled = true;
    status.textContent = "Đang tạo giọng đọc...";
    audio.style.display = "none";
    download.style.display = "none";

    try {

        const response = await fetch("/generate", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                text: text,
                speed: speed,
                spell: spell
            })

        });

        if (!response.ok) {

            const error = await response.json();

            throw new Error(
                error.error || "Không thể tạo âm thanh"
            );

        }

        const blob = await response.blob();
        const url = URL.createObjectURL(blob);

        audio.src = url;
        audio.style.display = "block";

        download.href = url;
        download.style.display = "inline-block";

        status.textContent = "Tạo âm thanh thành công!";

    } catch (error) {

        status.textContent = "Lỗi: " + error.message;

    } finally {

        button.disabled = false;

    }

}

</script>

</body>
</html>
"""


# =========================
# HOME ROUTE
# =========================

@app.route("/")
def home():
    return render_template_string(HTML)


# =========================
# GENERATE AUDIO ROUTE
# =========================

@app.route("/generate", methods=["POST"])
def generate():

    try:

        data = request.get_json(silent=True) or {}

        text = str(data.get("text", "")).strip()

        speed = data.get("speed", "normal")
        spell = data.get("spell", "normal")

        # Validate text
        if not text:
            return jsonify({
                "error": "Văn bản không được để trống"
            }), 400

        if len(text) > 4000:
            return jsonify({
                "error": "Văn bản tối đa 4000 ký tự"
            }), 400

        # Validate speed
        if speed not in ["normal", "slow"]:
            return jsonify({
                "error": "Tốc độ không hợp lệ"
            }), 400

        # Validate spelling
        if spell not in ["normal", "spell"]:
            return jsonify({
                "error": "Chế độ đánh vần không hợp lệ"
            }), 400

        # Process text
        processed_text = process_spelling(text, spell)

        print("Original text:", text)
        print("Processed text:", processed_text)
        print("Speed:", speed)
        print("Spell:", spell)

        # 1. Generate MP3 using Google TTS
        tts = gTTS(
            text=processed_text,
            lang="vi",
            slow=(speed == "slow")
        )

        mp3_buffer = BytesIO()
        tts.write_to_fp(mp3_buffer)

        mp3_data = mp3_buffer.getvalue()

        # 2. Convert MP3 to WAV using FFmpeg
        result = subprocess.run(
            [
                FFMPEG_PATH,
                "-y",
                "-hide_banner",
                "-loglevel", "error",
                "-i", "pipe:0",
                "-vn",
                "-acodec", "pcm_s16le",
                "-ar", "22050",
                "-ac", "1",
                "-f", "wav",
                "pipe:1"
            ],
            input=mp3_data,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )

        wav_data = result.stdout

        if not wav_data:
            raise Exception("FFmpeg không tạo được file WAV")

        # 3. Return WAV file
        wav_buffer = BytesIO(wav_data)
        wav_buffer.seek(0)

        return send_file(
            wav_buffer,
            mimetype="audio/wav",
            as_attachment=False,
            download_name="speech.wav"
        )

    except subprocess.CalledProcessError as e:

        error_detail = e.stderr.decode(
            "utf-8",
            errors="ignore"
        )

        print("FFmpeg Error:", error_detail)

        return jsonify({
            "error": "Lỗi chuyển đổi MP3 sang WAV"
        }), 500

    except Exception as e:

        print("TTS Error:", str(e))

        return jsonify({
            "error": "Không thể tạo giọng đọc. Vui lòng thử lại."
        }), 500


# =========================
# RUN SERVER
# =========================

if __name__ == "__main__":

    print("FFmpeg:", FFMPEG_PATH)

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
