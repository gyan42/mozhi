import json
import os
import io
import uuid

import cv2
from PIL import Image
from starlette.responses import Response

from fastapi import APIRouter
from fastapi import FastAPI, File, UploadFile
from api.internal.json_models import Text, ExtractedNER
import pytesseract

router = APIRouter()
STORE_PATH = '/tmp/mozhi/data'

@router.post("/mozhi/ocr/engine/pytesseract/file")
def pytesseract_engine(file: UploadFile = File(...)):
    print("running tesseract")
    file_bytes = file.file.read()
    image = Image.open(io.BytesIO(file_bytes))
    if os.path.exists(STORE_PATH):
        name = f"{STORE_PATH}/{str(uuid.uuid4())}_{file.filename}"
    else:
        os.makedirs(f'{STORE_PATH}/', exist_ok=True)
        name = f"{STORE_PATH}/{str(uuid.uuid4())}_{file.filename}"

    image.save(name)
    # predictions = resnext(image)
    custom_config = r'--oem 3 --psm 6'
    # tesseract_config = '-oem 2 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyz -c preserve_interword_spaces=1'
    img = cv2.imread(name)
    text = pytesseract.image_to_string(img, lang='eng', config=custom_config)
    print(json.dumps(text))
    # return {"text": text}
    return Response(content=json.dumps({"text": text}), media_type="application/json")
    # return Response(content=json.dumps(predictions), media_type="application/json")
    # return Response(file_bytes, media_type="image/jpg")
