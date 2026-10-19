from fastapi import UploadFile

class StorageService:
    def upload(self, file: UploadFile) -> str:
        raise NotImplementedError
