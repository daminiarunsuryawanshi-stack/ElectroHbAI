from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
import shutil
import os

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)


@router.post("/image")
def upload_image(
    file: UploadFile = File(...)
):

    os.makedirs("uploads", exist_ok=True)

    file_path = os.path.join(
        "uploads",
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "filename": file.filename,
        "image_url": f"/uploads/{file.filename}"
    }