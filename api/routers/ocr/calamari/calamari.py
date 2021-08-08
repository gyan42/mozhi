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

# import Craft class
from craft_text_detector import Craft


# from mozhi.ocr.text_detection import craft
from mozhi.ocr.text_extraction import calamari
from mozhi.ocr.text_stiching import combine_text_files


router = APIRouter()
TEMP_DATA_ROOT_PATH = '/tmp/mozhi'

craft_text_detection_craft = Craft(crop_type="poly", cuda=False)


def do_ocr(input_image_path, intermediate_path, file_name):
    """

    :param input_image_path: Absolute image to image file
    :param intermediate_path: Temp location to store craft files
    :param file_name: Image file name
    :return:
    """
    # craft.text_detection_craft(input_image_path=input_image_path,
    #                            output_dir=intermediate_path)

    craft_text_detection_craft.output_dir = intermediate_path
    # apply craft text detection and export detected regions to output directory
    prediction_result = craft_text_detection_craft.detect_text(input_image_path)

    sentences = calamari.handle_craft_intermediate_files(source_dir=intermediate_path + '/' + file_name.split(".")[0] + "_crops/")

    text = "\n".join(sentences)

    return text


# https://github.com/fcakyon/craft-text-detector
# Text Detection -> Calamari -> Text Stiching -> Display
@router.post("/mozhi/ocr/engine/calamari")
def calamri_engine(file: UploadFile = File(...)):
    file_bytes = file.file.read()
    image = Image.open(io.BytesIO(file_bytes))
    new_file_name = f"{str(uuid.uuid4())}_{file.filename}"

    if os.path.exists(TEMP_DATA_ROOT_PATH + '/data'):
        input_image_path = f"{TEMP_DATA_ROOT_PATH}/data/{new_file_name}"
    else:
        os.makedirs(f'{TEMP_DATA_ROOT_PATH}/data/', exist_ok=True)
        input_image_path = f"{TEMP_DATA_ROOT_PATH}/data/{new_file_name}"

    print(f"Storing the image in {input_image_path}")
    image.save(input_image_path)

    intermediate_path = f'{TEMP_DATA_ROOT_PATH}/craft/{new_file_name}/'

    text = do_ocr(input_image_path=input_image_path,
                  intermediate_path=intermediate_path,
                  file_name=new_file_name)
    # print(text)
    # return {"text": text}
    return Response(content=json.dumps({"text": text}), media_type="application/json")


if __name__ == '__main__':
    res = do_ocr(input_image_path="/data/receipts/X51008142068.jpg",
                 intermediate_path="/data/test/",
                 file_name="X51008142068")
    print(res)


"""
cd /path/to/mozhi
docker build -t mozhi-ocr-gpu:latest -f ops/docker/ocr/Dockerfile .
docker container  run -v $(pwd)/data:/data --network host --gpus all -it --rm --name mozhi-ocr-gpu mozhi-ocr-gpu:latest bash
python3 api/routers/ocr/calamari/calamari.py
"""