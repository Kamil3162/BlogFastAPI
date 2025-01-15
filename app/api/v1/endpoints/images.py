from fastapi import APIRouter
from fastapi import UploadFile, File
from fastapi.responses import Response
from starlette.responses import FileResponse

from ....storage.files import file_service

router = APIRouter()

@router.post('/images')
def upload_images(file_data: UploadFile = File(...)):
    print("file uploaded")
    file = file_service.save_file_and_update_record(file_data, "3")
    return Response(content=file, status_code=200)

@router.get('/images-list')
def upload_images():
    return Response(content="esa", status_code=200)

@router.get('/{image_id}')
def get_image(image_id: int):
    file_path, file = file_service.get_file_by_id(image_id)
    return FileResponse(
        file_path,
        media_type="image/jpeg",
        filename=file[0],
    )

@router.put('/change/{image_id}')
def change_image(file_data: UploadFile, image_id: int):
    file = file_service.change_file("3", file_data)
    print(file)

# shift shift
# ctl + e
# ctl + 1
# ctl tab
# ctl + R multiple change the same phrase
# ctl alt o optimize imports
# ctl + b - go to method or class implementation