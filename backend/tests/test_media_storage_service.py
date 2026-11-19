import io
import wave
import unittest
from types import SimpleNamespace

from fastapi import UploadFile
from minio.error import S3Error
from PIL import Image
from starlette.datastructures import Headers

from app.service.media_storage_service import (
    MediaNotFoundError,
    MediaStorageService,
    MediaTooLargeError,
    MediaValidationError,
)


class FakeMinio:
    def __init__(self):
        self.objects = {}
        self.fail_delete = set()

    def bucket_exists(self, _bucket):
        return True

    def put_object(self, _bucket, key, data, length, content_type, metadata):
        self.objects[key] = {
            "data": data.read(length),
            "content_type": content_type,
            "metadata": {f"x-amz-meta-{name}": value for name, value in metadata.items()},
        }

    def stat_object(self, _bucket, key):
        stored = self.objects.get(key)
        if stored is None:
            raise S3Error(None, "NoSuchKey", "Not found", key, None, None)
        return SimpleNamespace(
            content_type=stored["content_type"],
            size=len(stored["data"]),
            metadata=stored["metadata"],
        )

    def remove_object(self, _bucket, key):
        if key in self.fail_delete:
            raise RuntimeError("simulated storage failure")
        self.objects.pop(key, None)

    def presigned_get_object(self, _bucket, key, expires):
        return f"https://media.example/{key}?expires={int(expires.total_seconds())}"


def image_bytes(image_format="PNG"):
    output = io.BytesIO()
    Image.new("RGB", (4, 3), color="blue").save(output, format=image_format)
    return output.getvalue()


def wav_bytes():
    output = io.BytesIO()
    with wave.open(output, "wb") as audio:
        audio.setnchannels(1)
        audio.setsampwidth(2)
        audio.setframerate(16000)
        audio.writeframes(b"\x00\x00" * 1600)
    return output.getvalue()


def upload_file(name, content, content_type):
    return UploadFile(
        filename=name,
        file=io.BytesIO(content),
        headers=Headers({"content-type": content_type}),
    )


class MediaStorageServiceTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.service = MediaStorageService()
        self.fake = FakeMinio()
        self.service._client = self.fake
        self.service._url_client = self.fake

    async def test_upload_image_returns_uuid_key_and_signed_url(self):
        uploaded = await self.service.upload_file(
            upload_file("avatar.png", image_bytes(), "image/png"),
            "users/avatars/42",
            "image",
        )

        self.assertRegex(uploaded["object_key"], r"^users/avatars/42/[0-9a-f]{32}\.png$")
        self.assertEqual(uploaded["content_type"], "image/png")
        self.assertEqual(uploaded["filename"], "avatar.png")
        self.assertIn("expires=1800", uploaded["url"])
        self.assertEqual(len(self.fake.objects), 1)

    async def test_uploads_all_supported_image_formats(self):
        samples = [
            ("photo.jpg", image_bytes("JPEG"), "image/jpeg"),
            ("photo.jpeg", image_bytes("JPEG"), "image/jpeg"),
            ("photo.png", image_bytes("PNG"), "image/png"),
            ("photo.webp", image_bytes("WEBP"), "image/webp"),
        ]
        for filename, content, content_type in samples:
            with self.subTest(filename=filename):
                result = await self.service.upload_file(
                    upload_file(filename, content, content_type),
                    "topics/images",
                    "image",
                )
                self.assertEqual(result["content_type"], content_type)

    async def test_upload_wav_preserves_16khz_audio_and_metadata(self):
        uploaded = await self.service.upload_file(
            upload_file("sample.wav", wav_bytes(), "audio/x-wav"),
            "students/recordings/42",
            "audio",
        )

        self.assertEqual(uploaded["content_type"], "audio/wav")
        self.assertEqual(uploaded["sample_rate"], 16000)
        self.assertEqual(uploaded["channels"], 1)
        self.assertEqual(uploaded["duration"], 0.1)
        self.assertTrue(uploaded["object_key"].endswith(".wav"))

    async def test_uploads_all_supported_audio_signatures_without_conversion(self):
        samples = [
            ("voice.mp3", b"ID3\x04\x00\x00\x00\x00\x00\x00audio", "audio/mpeg"),
            ("voice.m4a", b"\x00\x00\x00\x18ftypM4A \x00\x00\x00\x00", "audio/mp4"),
            ("voice.ogg", b"OggS" + b"\x00" * 16, "audio/ogg"),
            ("voice.webm", b"\x1a\x45\xdf\xa3" + b"\x00" * 16, "audio/webm"),
        ]
        for filename, content, content_type in samples:
            with self.subTest(filename=filename):
                result = await self.service.upload_file(
                    upload_file(filename, content, content_type),
                    "lessons/audios",
                    "audio",
                )
                self.assertEqual(self.fake.objects[result["object_key"]]["data"], content)

    async def test_upload_many_rolls_back_prior_objects_on_failure(self):
        with self.assertRaises(MediaValidationError):
            await self.service.upload_many(
                [
                    upload_file("good.png", image_bytes(), "image/png"),
                    upload_file("fake.png", b"not an image", "image/png"),
                ],
                "products/images",
                "image",
            )
        self.assertEqual(self.fake.objects, {})

    async def test_metadata_lookup_and_delete(self):
        uploaded = await self.service.upload_file(
            upload_file("ảnh.png", image_bytes(), "image/png"),
            "lessons/images",
            "image",
        )

        metadata = self.service.get_file_metadata(uploaded["object_key"])
        self.assertEqual(metadata["filename"], "ảnh.png")
        self.assertEqual(metadata["media_type"], "image")
        self.assertEqual(metadata["file_size"], uploaded["file_size"])
        self.service.delete_file(uploaded["object_key"])
        self.assertFalse(self.service.object_exists(uploaded["object_key"]))

    async def test_rejects_mime_extension_content_and_traversal_mismatches(self):
        with self.assertRaises(MediaValidationError):
            await self.service.upload_file(
                upload_file("avatar.jpg", image_bytes(), "image/jpeg"),
                "users/avatars/42",
                "image",
            )
        with self.assertRaises(MediaValidationError):
            await self.service.upload_file(
                upload_file("avatar.png", b"not an image", "image/png"),
                "users/avatars/42",
                "image",
            )
        with self.assertRaises(MediaValidationError):
            await self.service.upload_file(
                upload_file("avatar.png", image_bytes(), "audio/wav"),
                "users/avatars/42",
                "image",
            )
        with self.assertRaises(MediaValidationError):
            await self.service.upload_file(
                upload_file("avatar.png", image_bytes(), "image/png"),
                "users/../other",
                "image",
            )

    async def test_upload_limit_and_multi_delete_partial_failure(self):
        from app.config.config import settings

        original_max_size = settings.media_image_max_bytes
        settings.media_image_max_bytes = 16
        try:
            with self.assertRaises(MediaTooLargeError):
                await self.service.upload_file(
                    upload_file("avatar.png", image_bytes(), "image/png"),
                    "users/avatars/42",
                    "image",
                )
        finally:
            settings.media_image_max_bytes = original_max_size

        self.fake.objects["students/recordings/ok.wav"] = {
            "data": b"data",
            "content_type": "audio/wav",
            "metadata": {},
        }
        self.fake.objects["students/recordings/fail.wav"] = {
            "data": b"data",
            "content_type": "audio/wav",
            "metadata": {},
        }
        self.fake.fail_delete.add("students/recordings/fail.wav")
        result = self.service.delete_many(
            ["students/recordings/ok.wav", "students/recordings/fail.wav"]
        )

        self.assertEqual(result["deleted"], ["students/recordings/ok.wav"])
        self.assertEqual(result["failed"], ["students/recordings/fail.wav"])

    async def test_missing_object_is_reported(self):
        with self.assertRaises(MediaNotFoundError):
            self.service.delete_file("missing/object.wav")


if __name__ == "__main__":
    unittest.main()
