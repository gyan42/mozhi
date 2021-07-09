import io
import sys
import os
import json
import uuid
import cv2
import pytesseract
import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi import APIRouter
from PIL import Image

from starlette.responses import Response

from mozhi.ocr.text_detection import craft
from mozhi.ocr.text_extraction import calamari
from mozhi.ocr.text_stiching import combine_text_files


router = APIRouter()
STORE_PATH = '/tmp/mozhi/data'


# https://github.com/fcakyon/craft-text-detector
# Text Detection -> Calamari -> Text Stiching -> Display
@router.post("/mozhi/ocr/engine/calamari")
def calamri_engine(file: UploadFile = File(...)):
    file_bytes = file.file.read()
    image = Image.open(io.BytesIO(file_bytes))
    new_file_name = f"{str(uuid.uuid4())}_{file.filename}"
    if os.path.exists(STORE_PATH):
        name = f"{STORE_PATH}/{new_file_name}"
    else:
        os.makedirs(f'{STORE_PATH}/', exist_ok=True)
        name = f"{STORE_PATH}/{new_file_name}"

    image.save(name)

    input_image_path = name
    intermediate_path = f"/tmp/vf/craft/{new_file_name}/"
    text_out_path = f"/tmp/vf/output/{new_file_name}"
    out_text_file_path = f"/tmp/vf/output/text/"

    if not os.path.exists(out_text_file_path):
        os.makedirs(out_text_file_path)

    out_text_file_path = f"{out_text_file_path}/{new_file_name}.txt"

    craft.text_detection_craft(input_image_path=input_image_path,
                               output_dir=intermediate_path)

    calamari.handle_files(source_dir=intermediate_path,
                          destination_dir=text_out_path)

    # TODO file name with multiple `.` may go for toss
    combine_text_files.handle_file(input_txt_files_dir=text_out_path+f'/{new_file_name.split(".")[0]}_crops/',
                                   out_file_path=out_text_file_path)

    text = "".join(open(out_text_file_path, "r").readlines())

    # return {"text": text}
    return Response(content=json.dumps({"text": text}), media_type="application/json")