from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import numpy as np
from typing import List
import cv2
from service import FaceService
import logging
from fastapi import Form
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import json



logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)


class LimitUploadSizeMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_part_size: int):
        super().__init__(app)
        self.max_part_size = max_part_size

    async def dispatch(self, request, call_next):
        # Chỉ check multipart
        if "multipart/form-data" in request.headers.get("content-type", ""):
            body = await request.body()
            if len(body) > self.max_part_size:
                return JSONResponse(
                    {"detail": f"Part exceeded maximum size of {self.max_part_size} bytes."},
                    status_code=413
                )
        return await call_next(request)


app = FastAPI()
service = FaceService()
app.add_middleware(LimitUploadSizeMiddleware, max_part_size=50 * 1024 * 1024)

# ---- Model cho request ----
class RegisterRequest(BaseModel):
    user_id: str
    # landmarks_list: list of list of 487 points (list of floats)
    landmarks_list: list[list[list[float]]]  

class RecognizeRequest(BaseModel):
    # landmarks: list of 487 points
    landmarks: list[list[float]]  

# ---- Helper để convert bytes image thành numpy array ----
def read_image(file: UploadFile):
    img_bytes = file.file.read()
    img_array = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return img

# ---- API đăng ký ----
@app.post("/register")
async def register(
    user_id: str = Form(...),
    landmarks: str = Form(...),
    files: List[UploadFile] = File(...)
):
    
    try:
        lm10s = json.loads(landmarks)
        images = [read_image(f) for f in files]
        res = service.register(images, lm10s, user_id)
        print(res)
        return res
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return {"error": str(e)}


@app.post("/recognize")
async def recognize(
    file: UploadFile = File(...),
    landmarks: str = Form(...)
):
    try:
        img = read_image(file)
        lm10 = json.loads(landmarks)
        
        res = service.recognize(img, lm10)
        print(res)
        return res
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return {"error": str(e)}



