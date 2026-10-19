import uuid 
from pathlib import Path

from fastapi import HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError
from io import BytesIO


UPLOAD_DIR = Path("media/profile-images")
MAX_FILE_SIZE = 5 * 1024 * 1024

ALLOWED_FORMATS = {
    "JPG": ".jpg",
    "JPEG": ".jpeg",
    "PNG": ".png",
    "WEBP": ".webp",
}

def save_profile_image(file: UploadFile) -> str:
    data = file.file.read(MAX_FILE_SIZE + 1)

    if len(data) > MAX_FILE_SIZE:
        raise HTTPException(
            detail=f"Image must not exceed 5mb",
            status_code=413,
        )

    try:
        with Image.open(BytesIO(data)) as image:
            image.verify()

        with Image.open(BytesIO(data)) as image:
            image_format = image.format

    except (UnidentifiedImageError, OSError) as er:
        print(f"save_profile_image error:: {er}")
        raise HTTPException(
            detail="Invalid image file",
            status_code=422
        )

    extension = ALLOWED_FORMATS.get(image_format)

    if extension is None:
        raise HTTPException(
            detail="Only JPG, JPEG, PNG, and WEBP are allowed",
            status_code=422
        )

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    filename = f"{uuid.uuid4().hex}{extension}"
    destination = UPLOAD_DIR / filename

    destination.write_bytes(data)

    return f"/media/profile-images/{filename}"
