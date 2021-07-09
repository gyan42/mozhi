import base64
import io
import os
import uuid
from typing import Optional
import fastapi
from fastapi import APIRouter
from starlette.responses import Response
import urllib3.response
from PIL import Image
from api.internal.json_models import StorageAuthentication
import pandas as pd
import psycopg2
import json
router = APIRouter()
import boto3
from botocore.client import Config
client = None
from starlette.responses import StreamingResponse
from minio import Minio
# from fastapi.responses import
import cv2
import pytesseract
from pytesseract import Output

STORE_PATH = '/tmp/mozhi/data'

@router.post("/mozhi/storage/minio/list")
def list_prefixes(data: StorageAuthentication):
    global client
    if client is None:
        client = Minio(endpoint=data.host + ":" + data.port,
                       access_key=data.accessKey,
                       secret_key=data.secretKey,
                       secure=False)
        # client = boto3.resource('s3',
        #             endpoint_url='http://localhost:9000',
        #             aws_access_key_id=data.accessKey,
        #             aws_secret_access_key=data.secretKey,
        #             config=Config(signature_version='s3v4'),
        #             region_name='us-east-1')

    objects = client.list_objects(data.bucket,
                                  prefix=data.prefix,
                                  recursive=True)

    files = []
    for obj in objects:
        files.append(obj.object_name)
        # print(obj.bucket_name,
        #       obj.object_name.encode('utf-8'),
        #       obj.last_modified,
        #       obj.etag,
        #       obj.size,
        #       obj.content_type)
    print(files)
    return files


@router.get("/mozhi/storage/minio/get/image")
def get_file(bucket: str, file_prefix: str):
    if client is None:
        return {"data": ""}
    response: urllib3.HTTPResponse = client.get_object(bucket, file_prefix)
    # print(response.headers)
    # print(type(response.data))
    # print(io.BytesIO(data.data).read())
    # print(base64.b64encode(io.BytesIO(data.data).getvalue()).decode())
    return StreamingResponse(io.BytesIO(response.data),
                             headers=response.headers,
                             media_type=response.headers["content-type"])
    # return {"base64" : base64.b64encode(io.BytesIO(response.data).getvalue()).decode()}
    # return fastapi.responses.Response(content=response.data,
    #                                   headers=response.headers,
    #                                   media_type=response.headers["content-type"])


@router.get("/mozhi/storage/minio/get/text/")
def get_text(bucket: str, file_prefix: str):
    if client is None:
        return {"data": ""}
    response: urllib3.HTTPResponse = client.get_object(bucket, file_prefix)
    image = Image.open(io.BytesIO(response.data))

    if os.path.exists(STORE_PATH):
        name = f"{STORE_PATH}/{str(uuid.uuid4())}_{file_prefix.split('/')[-1]}"
    else:
        os.makedirs(f'{STORE_PATH}/', exist_ok=True)
        name = f"{STORE_PATH}/{str(uuid.uuid4())}_{file_prefix.split('/')[-1]}"

    image.save(name)
    # predictions = resnext(image)
    custom_config = r'--oem 3 --psm 6'
    # tesseract_config = '-oem 2 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyz -c preserve_interword_spaces=1'
    img = cv2.imread(name)
    text = pytesseract.image_to_string(img, lang='eng', config=custom_config)
    print(json.dumps(text))
    # return {"text": text}
    return Response(content=json.dumps({"text": text}), media_type="application/json")

def extract_bbox(results):
    res = []
    for i in range(0, len(results["text"])):
        # extract the bounding box coordinates of the text region from
        # the current result
        x = results["left"][i]
        y = results["top"][i]
        w = results["width"][i]
        h = results["height"][i]
        # extract the OCR text itself along with the confidence of the
        # text localization
        text = results["text"][i]
        conf = int(results["conf"][i])
        if len(text)>0:
            res.append((x, y, w, h, text))
    return res

@router.get("/mozhi/storage/minio/get/textinfo/")
def get_text(bucket: str, file_prefix: str):
    if client is None:
        return {"data": ""}
    response: urllib3.HTTPResponse = client.get_object(bucket, file_prefix)
    image = Image.open(io.BytesIO(response.data))

    if os.path.exists(STORE_PATH):
        name = f"{STORE_PATH}/{str(uuid.uuid4())}_{file_prefix.split('/')[-1]}"
    else:
        os.makedirs(f'{STORE_PATH}/', exist_ok=True)
        name = f"{STORE_PATH}/{str(uuid.uuid4())}_{file_prefix.split('/')[-1]}"

    image.save(name)
    img = cv2.imread(name)
    results = pytesseract.image_to_data(img, output_type=Output.DICT)
    print(results)
    print(extract_bbox(results))
    # return {"text": text}
    return Response(content=json.dumps({"textinfo": results}), media_type="application/json")