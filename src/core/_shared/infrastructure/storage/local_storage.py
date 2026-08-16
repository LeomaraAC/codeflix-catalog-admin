from pathlib import Path

from src.core._shared.infrastructure.storage.abstract_storage_service import AbstractStorageService


class LocalStorage(AbstractStorageService):
    TMP_BUCKET = '/tmp/codeflix-storage'

    def __init__(self, bucket: str = TMP_BUCKET):
        self.bucket = Path(bucket)
        self.bucket.mkdir(parents=True, exist_ok=True)

    def store(self, file_path: str, content: bytes, content_type: str):
        full_path = self.bucket / file_path

        full_path.parent.mkdir(parents=True, exist_ok=True)
        with open(full_path, 'wb') as f:
            f.write(content)
