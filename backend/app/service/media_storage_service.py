import base64
import io
import logging
import re
import wave
from datetime import datetime
from urllib.parse import quote
import zipfile
from pathlib import PurePosixPath
from typing import Literal, Sequence
from uuid import uuid4

from fastapi import UploadFile
from minio import Minio
from minio.error import S3Error
from PIL import Image, UnidentifiedImageError

from app.config.config import settings

logger = logging.getLogger(__name__)

MediaType = Literal["image", "audio"]

IMAGE_TYPES = {
    ".jpg": ("image/jpeg", "JPEG"),
    ".jpeg": ("image/jpeg", "JPEG"),
    ".png": ("image/png", "PNG"),
    ".webp": ("image/webp", "WEBP"),
}
AUDIO_TYPES = {
    ".mp3": ("audio/mpeg", "mp3"),
    ".wav": ("audio/wav", "wav"),
    ".m4a": ("audio/mp4", "m4a"),
    ".ogg": ("audio/ogg", "ogg"),
    ".webm": ("audio/webm", "webm"),
}
WAV_CONTENT_TYPES = {"audio/wav", "audio/x-wav"}


class MediaStorageError(Exception):
    """Raised when an object-storage operation fails."""


class MediaValidationError(ValueError):
    """Raised when a media file or object key is invalid."""


class MediaTooLargeError(MediaValidationError):
    """Raised when an upload exceeds the configured per-media size limit."""


class MediaNotFoundError(MediaStorageError):
    """Raised when a requested object does not exist."""


class MediaStorageService:
    """Store validated images and audio in the configured private MinIO bucket."""

    def __init__(self) -> None:
        self._client = self._create_client(settings.minio_endpoint, settings.minio_secure)
        public_endpoint = settings.minio_public_endpoint or settings.minio_endpoint
        self._url_client = self._create_client(public_endpoint, settings.minio_secure)

    @staticmethod
    def _create_client(endpoint: str, secure: bool) -> Minio:
        return Minio(
            endpoint,
            access_key=settings.minio_root_user,
            secret_key=settings.minio_root_password,
            secure=secure,
        )

    @staticmethod
    def _safe_folder(folder: str) -> str:
        normalized = folder.strip("/")
        if not normalized or "\\" in normalized:
            raise MediaValidationError("Thư mục lưu trữ không hợp lệ.")
        parts = normalized.split("/")
        if any(
            not part
            or part in {".", ".."}
            or not re.fullmatch(r"[A-Za-z0-9._-]+", part)
            for part in parts
        ):
            raise MediaValidationError("Thư mục lưu trữ không hợp lệ.")
        return str(PurePosixPath(*parts))

    @staticmethod
    def _safe_object_key(object_key: str) -> str:
        if not isinstance(object_key, str) or not object_key or "\\" in object_key:
            raise MediaValidationError("Định danh file không hợp lệ.")
        parts = object_key.split("/")
        if any(
            not part
            or part in {".", ".."}
            or not re.fullmatch(r"[A-Za-z0-9._-]+", part)
            for part in parts
        ):
            raise MediaValidationError("Định danh file không hợp lệ.")
        return str(PurePosixPath(*parts))

    @staticmethod
    def _safe_filename(filename: str | None) -> str:
        if not filename:
            raise MediaValidationError("File không có tên hợp lệ.")
        name = filename.replace("\\", "/").rsplit("/", 1)[-1]
        if not name or name in {".", ".."} or any(ord(char) < 32 for char in name):
            raise MediaValidationError("File không có tên hợp lệ.")
        return name

    @staticmethod
    def _assert_content(
        data: bytes,
        extension: str,
        content_type: str | None,
        media_type: MediaType,
    ) -> tuple[str, str]:
        supported_types = IMAGE_TYPES if media_type == "image" else AUDIO_TYPES
        expected = supported_types.get(extension)
        if expected is None:
            raise MediaValidationError("Định dạng file không được hỗ trợ.")

        expected_type, detected_format = expected
        actual_type = (content_type or "").split(";", 1)[0].strip().lower()
        allowed_types = (
            WAV_CONTENT_TYPES if extension == ".wav" else {expected_type}
        )
        if actual_type not in allowed_types:
            raise MediaValidationError("MIME type không khớp với phần mở rộng file.")

        if media_type == "image":
            try:
                with Image.open(io.BytesIO(data)) as image:
                    if image.format != detected_format:
                        raise MediaValidationError("Nội dung ảnh không khớp với phần mở rộng.")
                    if image.width * image.height > 40_000_000:
                        raise MediaValidationError("Kích thước ảnh vượt quá giới hạn cho phép.")
                    image.verify()
            except (UnidentifiedImageError, OSError, Image.DecompressionBombError) as error:
                raise MediaValidationError("Nội dung ảnh không hợp lệ.") from error
        else:
            MediaStorageService._assert_audio_signature(data, extension)

        return expected_type, detected_format

    @staticmethod
    def _assert_audio_signature(data: bytes, extension: str) -> None:
        valid = False
        if extension == ".wav":
            MediaStorageService._validate_wav(data)
            valid = True
        elif extension == ".mp3":
            valid = data.startswith(b"ID3") or (
                len(data) >= 2 and data[0] == 0xFF and data[1] & 0xE0 == 0xE0
            )
        elif extension == ".m4a":
            valid = (
                len(data) >= 16
                and data[4:8] == b"ftyp"
                and any(brand in data[8:64] for brand in (b"M4A ", b"M4B ", b"M4P "))
            )
        elif extension == ".ogg":
            valid = data.startswith(b"OggS")
        elif extension == ".webm":
            valid = data.startswith(b"\x1a\x45\xdf\xa3")
        if not valid:
            raise MediaValidationError("Nội dung âm thanh không khớp với phần mở rộng.")

    @staticmethod
    def _validate_wav(data: bytes) -> None:
        if len(data) < 44 or data[:4] != b"RIFF" or data[8:12] != b"WAVE":
            raise MediaValidationError("Nội dung âm thanh không khớp với phần mở rộng.")
        riff_end = int.from_bytes(data[4:8], "little") + 8
        if riff_end > len(data) or riff_end < 12:
            raise MediaValidationError("File WAV không hợp lệ.")

        has_format = False
        has_audio_data = False
        offset = 12
        while offset + 8 <= riff_end:
            chunk_id = data[offset:offset + 4]
            chunk_size = int.from_bytes(data[offset + 4:offset + 8], "little")
            chunk_start = offset + 8
            chunk_end = chunk_start + chunk_size
            if chunk_end > riff_end:
                raise MediaValidationError("File WAV không hợp lệ.")
            if chunk_id == b"fmt " and chunk_size >= 16:
                has_format = True
            elif chunk_id == b"data" and chunk_size > 0:
                has_audio_data = True
            offset = chunk_end + (chunk_size & 1)

        if not has_format or not has_audio_data:
            raise MediaValidationError("File WAV thiếu thông tin âm thanh cần thiết.")

    @staticmethod
    def _wav_metadata(data: bytes) -> dict[str, int | float]:
        try:
            with wave.open(io.BytesIO(data), "rb") as wav_file:
                sample_rate = wav_file.getframerate()
                frame_count = wav_file.getnframes()
                return {
                    "sample_rate": sample_rate,
                    "channels": wav_file.getnchannels(),
                    "duration": round(frame_count / sample_rate, 3) if sample_rate else 0,
                }
        except (wave.Error, EOFError):
            return {}

    def _ensure_bucket(self) -> None:
        if self._client.bucket_exists(settings.minio_bucket_name):
            return
        try:
            self._client.make_bucket(settings.minio_bucket_name)
        except Exception:
            if not self._client.bucket_exists(settings.minio_bucket_name):
                raise

    async def upload_file(
        self,
        file: UploadFile,
        folder: str,
        media_type: MediaType,
    ) -> dict:
        if media_type not in {"image", "audio"}:
            raise MediaValidationError("Loại media không được hỗ trợ.")
        safe_folder = self._safe_folder(folder)
        filename = self._safe_filename(file.filename)
        extension = PurePosixPath(filename).suffix.lower()
        max_size = (
            settings.media_image_max_bytes
            if media_type == "image"
            else settings.media_audio_max_bytes
        )
        try:
            data = await file.read(max_size + 1)
        except Exception as error:
            raise MediaStorageError("Không thể đọc nội dung file tải lên.") from error
        if not data:
            raise MediaValidationError("File không được để trống.")
        if len(data) > max_size:
            raise MediaTooLargeError("Dung lượng file vượt quá giới hạn cho phép.")

        content_type, file_format = self._assert_content(
            data,
            extension,
            file.content_type,
            media_type,
        )
        object_key = f"{safe_folder}/{uuid4().hex}{extension}"
        metadata = {
            "media-type": media_type,
            "original-filename-b64": base64.urlsafe_b64encode(
                filename.encode("utf-8")
            ).decode("ascii"),
            "format": file_format,
        }
        audio_metadata = self._wav_metadata(data) if extension == ".wav" else {}
        if audio_metadata:
            metadata.update(
                {
                    "sample-rate": str(audio_metadata["sample_rate"]),
                    "channels": str(audio_metadata["channels"]),
                    "duration": str(audio_metadata["duration"]),
                }
            )

        uploaded_to_bucket = False
        try:
            self._ensure_bucket()
            self._client.put_object(
                settings.minio_bucket_name,
                object_key,
                io.BytesIO(data),
                length=len(data),
                content_type=content_type,
                metadata=metadata,
            )
            uploaded_to_bucket = True
            url = self.get_file_url(object_key)
        except Exception as error:
            logger.exception("MinIO upload failed.")
            if uploaded_to_bucket:
                try:
                    self._client.remove_object(settings.minio_bucket_name, object_key)
                except Exception:
                    logger.exception("Could not clean up an incomplete media upload.")
            raise MediaStorageError("Không thể lưu file vào kho media.") from error

        return {
            "object_key": object_key,
            "filename": filename,
            "content_type": content_type,
            "media_type": media_type,
            "file_size": len(data),
            "url": url,
            **audio_metadata,
            "format": file_format,
        }

    async def upload_document(self, file: UploadFile, folder: str) -> dict:
        """Validate and store a private expert application document."""
        safe_folder = self._safe_folder(folder)
        filename = self._safe_filename(file.filename)
        extension = PurePosixPath(filename).suffix.lower()
        content_types = {
            ".pdf": ("application/pdf",),
            ".docx": ("application/vnd.openxmlformats-officedocument.wordprocessingml.document",),
            ".jpg": ("image/jpeg",), ".jpeg": ("image/jpeg",),
            ".png": ("image/png",), ".webp": ("image/webp",),
            ".xls": ("application/vnd.ms-excel", "application/octet-stream"),
            ".xlsx": ("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",),
        }
        allowed = content_types.get(extension)
        if not allowed:
            raise MediaValidationError("Unsupported document format.")
        limit = 10 * 1024 * 1024
        try:
            data = await file.read(limit + 1)
        except Exception as error:
            raise MediaStorageError("Could not read uploaded document.") from error
        if not data:
            raise MediaValidationError("The file is empty.")
        if len(data) > limit:
            raise MediaTooLargeError("Each document must be 10 MiB or smaller.")
        declared_type = (file.content_type or "").split(";", 1)[0].strip().lower()
        generic_types = {"", "application/octet-stream", "binary/octet-stream"}
        if declared_type not in allowed and declared_type not in generic_types:
            raise MediaValidationError("MIME type does not match the file extension.")
        # Browsers and operating systems often report a generic MIME type for valid
        # local files. The signature/content checks below remain authoritative.
        actual_type = allowed[0] if declared_type in generic_types else declared_type

        valid = False
        if extension == ".pdf":
            # Some valid PDFs contain a short preamble before the header. Readers
            # commonly tolerate the header anywhere in the first 1024 bytes.
            valid = b"%PDF-" in data[:1024]
        elif extension == ".xls":
            valid = data.startswith(bytes.fromhex("D0CF11E0A1B11AE1"))
        elif extension in {".docx", ".xlsx"}:
            required = {
                ".docx": "word/document.xml",
                ".xlsx": "xl/workbook.xml",
            }[extension]
            try:
                with zipfile.ZipFile(io.BytesIO(data)) as archive:
                    valid = "[Content_Types].xml" in archive.namelist() and required in archive.namelist()
            except (zipfile.BadZipFile, OSError):
                valid = False
        elif extension in {".jpg", ".jpeg", ".png", ".webp"}:
            expected = {".jpg": "JPEG", ".jpeg": "JPEG", ".png": "PNG", ".webp": "WEBP"}[extension]
            try:
                with Image.open(io.BytesIO(data)) as image:
                    valid = image.format == expected
                    image.verify()
            except (UnidentifiedImageError, OSError, Image.DecompressionBombError):
                valid = False
        if not valid:
            raise MediaValidationError("File content does not match the declared format.")

        object_key = f"{safe_folder}/{uuid4().hex}{extension}"
        metadata = {
            "media-type": "document",
            "original-filename-b64": base64.urlsafe_b64encode(filename.encode("utf-8")).decode("ascii"),
        }
        try:
            self._ensure_bucket()
            self._client.put_object(
                settings.minio_bucket_name, object_key, io.BytesIO(data),
                length=len(data), content_type=actual_type, metadata=metadata,
            )
        except Exception as error:
            logger.exception("MinIO document upload failed.")
            raise MediaStorageError("Could not store document in MinIO.") from error
        return {
            "object_key": object_key,
            "filename": filename,
            "content_type": actual_type,
            "file_size": len(data),
            "uploaded_at": datetime.utcnow().isoformat(),
        }

    async def upload_many(
        self,
        files: Sequence[UploadFile],
        folder: str,
        media_type: MediaType,
    ) -> list[dict]:
        uploaded: list[dict] = []
        try:
            for file in files:
                uploaded.append(await self.upload_file(file, folder, media_type))
        except Exception:
            for item in uploaded:
                try:
                    self.delete_file(item["object_key"])
                except Exception:
                    logger.exception("Failed to roll back a partially completed media upload.")
            raise
        return uploaded

    def object_exists(self, object_key: str) -> bool:
        safe_key = self._safe_object_key(object_key)
        try:
            self._client.stat_object(settings.minio_bucket_name, safe_key)
            return True
        except S3Error as error:
            if error.code in {"NoSuchKey", "NoSuchObject", "NotFound"}:
                return False
            logger.exception("MinIO metadata lookup failed.")
            raise MediaStorageError("Không thể kiểm tra file trong kho media.") from error
        except Exception as error:
            logger.exception("MinIO metadata lookup failed.")
            raise MediaStorageError("Không thể kiểm tra file trong kho media.") from error

    def delete_file(self, object_key: str) -> None:
        safe_key = self._safe_object_key(object_key)
        if not self.object_exists(safe_key):
            raise MediaNotFoundError("Không tìm thấy file trong kho media.")
        try:
            self._client.remove_object(settings.minio_bucket_name, safe_key)
        except Exception as error:
            logger.exception("MinIO delete failed.")
            raise MediaStorageError("Không thể xóa file khỏi kho media.") from error

    def delete_many(self, object_keys: Sequence[str]) -> dict[str, list]:
        deleted: list[str] = []
        failed: list[str] = []
        for object_key in object_keys:
            try:
                self.delete_file(object_key)
                deleted.append(object_key)
            except Exception:
                logger.exception("Failed to delete a media object.")
                failed.append(object_key)
        return {"deleted": deleted, "failed": failed}

    def get_file_url(self, object_key: str, download_name: str | None = None, force_download: bool = False) -> str:
        safe_key = self._safe_object_key(object_key)
        expiry_seconds = settings.media_url_expiry_seconds
        if not 1 <= expiry_seconds <= 604800:
            raise MediaStorageError("Thời hạn URL media phải nằm trong 1..604800 giây.")
        try:
            if not self.object_exists(safe_key):
                raise MediaNotFoundError("Không tìm thấy file trong kho media.")
            from datetime import timedelta

            response_headers = None
            if download_name:
                safe_name = self._safe_filename(download_name)
                disposition = "attachment" if force_download else "inline"
                response_headers = {
                    "response-content-disposition": f"{disposition}; filename*=UTF-8''{quote(safe_name)}"
                }
            return self._url_client.presigned_get_object(
                settings.minio_bucket_name,
                safe_key,
                expires=timedelta(seconds=expiry_seconds),
                response_headers=response_headers,
            )
        except MediaNotFoundError:
            raise
        except Exception as error:
            logger.exception("MinIO URL signing failed.")
            raise MediaStorageError("Không thể tạo URL truy cập file.") from error

    def get_file_metadata(self, object_key: str) -> dict:
        safe_key = self._safe_object_key(object_key)
        try:
            stat = self._client.stat_object(settings.minio_bucket_name, safe_key)
        except S3Error as error:
            if error.code in {"NoSuchKey", "NoSuchObject", "NotFound"}:
                raise MediaNotFoundError("Không tìm thấy file trong kho media.") from error
            logger.exception("MinIO metadata lookup failed.")
            raise MediaStorageError("Không thể đọc thông tin file.") from error
        except Exception as error:
            logger.exception("MinIO metadata lookup failed.")
            raise MediaStorageError("Không thể đọc thông tin file.") from error

        stored_metadata = {
            key.lower().removeprefix("x-amz-meta-"): value
            for key, value in (stat.metadata or {}).items()
        }
        filename = stored_metadata.get("original-filename-b64")
        result = {
            "object_key": safe_key,
            "filename": (
                base64.urlsafe_b64decode(filename.encode("ascii")).decode("utf-8")
                if filename
                else PurePosixPath(safe_key).name
            ),
            "content_type": stat.content_type,
            "media_type": stored_metadata.get("media-type"),
            "file_size": stat.size,
            "url": self.get_file_url(safe_key),
            "format": stored_metadata.get("format"),
        }
        for key in ("duration", "sample-rate", "channels"):
            if key in stored_metadata:
                value: int | float = (
                    float(stored_metadata[key]) if key == "duration"
                    else int(stored_metadata[key])
                )
                result[key.replace("-", "_")] = value
        return result


media_storage_service = MediaStorageService()
