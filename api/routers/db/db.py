import io
import os
import uuid
import json
from typing import List
from fastapi import APIRouter, Body, File, UploadFile, Form
from api.internal.json_models import AnnotatedData, DBServer, DBConnectionInfo
import pandas as pd
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import json
from pydantic import BaseModel
from sqlalchemy import create_engine

from mozhi.db.conll_upload import upload_text_data

router = APIRouter()

connection = None
STORE_PATH = '/tmp/mozhi/data/db'

@router.post("/mozhi/db/create")
def create_table(connection_info: DBConnectionInfo, dbname: str):
    try:
        connection = psycopg2.connect(host=connection_info.host,
                                      port=connection_info.port,
                                      database=connection_info.dbname,
                                      user=connection_info.user,
                                      password=connection_info.password)
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = connection.cursor()

        # Use the psycopg2.sql module instead of string concatenation
        # in order to avoid sql injection attacs.
        cur.execute(sql.SQL("CREATE DATABASE {};").format(
                sql.Identifier(dbname))
            )
        return {"status": "Success"}
    except Exception as e:
        print(e)
        return {"status": "Failed"}

# https://stackoverflow.com/questions/65510798/how-can-i-upload-multiple-files-using-javascript-and-fastapi/65513660#65513660
@router.post("/mozhi/db/upload/textfiles")
def upload_text_files(connection_info=Form(...), files: List[UploadFile] = File(...)):
    res = []
    new_dir = f"{STORE_PATH}/{str(uuid.uuid4())}"
    os.makedirs(new_dir)

    for file in files:
        file_bytes = file.file.read()
        bytesio_object = io.BytesIO(file_bytes)
        name = f"{new_dir}/{file.filename}"
        res.append(name)
        with open(name, "wb") as f:
            f.write(bytesio_object.getbuffer())
    # TODO find a better way to handle file upload and connection info
    connection_info: DBConnectionInfo = json.loads(connection_info)
    user = connection_info['user']
    password = connection_info['password']
    host = connection_info['host']
    port = connection_info['port']
    db_name = connection_info['dbname']
    upload_text_data(dir_root_path="/tmp/mozhi/data/db/22a607f2-0c90-4fd4-afd6-1c1031ac2c3f",
                     is_delete=True,
                     engine=create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}'),
                     experiment_name="conll20031")
    return {"uploadedpath": new_dir}


# ------------------------------------------------------------------------------------------------------------------------

@router.post("/mozhi/db/text/get/tags")  # TODO make it as get/query
def get_table(data: DBConnectionInfo):
    global connection
    print(data)
    conn = psycopg2.connect(host=data.host,
                            port=data.port,
                            database=data.db_name,
                            user=data.user,
                            password=data.password)
    connection = conn
    sql_command = f"SELECT * FROM \"{data.tag_table_name}\";"

    df = pd.read_sql(sql_command, conn)
    tags = df["name"].to_list()
    return {"tags": tags}


@router.post("/mozhi/db/text/table/{row_id}") #  TODO make it as get/query
def get_row(row_id: int, data: DBConnectionInfo):
    global connection
    if connection is None:
        connection = psycopg2.connect(host=data.host,
                                      port=data.port,
                                      database=data.db_name,
                                      user=data.user,
                                      password=data.password)
    sql_command = f"SELECT * FROM \"{data.text_table_name}\" where id = {row_id};"
    print(sql_command)
    df = pd.read_sql(sql_command, connection)
    print("*"*100)
    print(sql_command)
    print(df)
    if len(df) > 0:
        # if annotations are found create a list of dict with relevant information for Vue TokenManager
        if "features" in df.columns:
            res = []
            words = df["features"][0].split(" ")
            tags = df["labels"][0].split(" ")
            print(len(words), len(tags), words, tags)
            if len(words) > 1 and len(tags) > 1:
                i = 0
                for w, t in zip(words, tags):
                    # Spacy format for NER tags
                    res.append({"start": i, "end": i + len(t), "text": w, "type": "label", "label": t})
                    i = i + len(t) + 1
                res = {"text": df["text"][0], "features": df["features"][0], "labels":  df["labels"][0], "annotated": json.dumps(res)}
            else:
                res = {"text": df["text"][0], "features": "", "labels": ""}
        else:
            res = {"text": df["text"][0], "features": "", "labels": ""}
    else:
        res = {"text":"", "features": "", "labels": ""}
    print(res)
    return res


@router.post("/mozhi/db/text/get/counts")
def get_total_rows(connection_info: DBConnectionInfo, text_table_name: str):
    connection = psycopg2.connect(host=connection_info.host,
                                  port=connection_info.port,
                                  database=connection_info.dbname,
                                  user=connection_info.user,
                                  password=connection_info.password)
    sql_command = f"SELECT count(*) as count FROM \"{text_table_name}\";"

    df = pd.read_sql(sql_command, connection)
    res = df["count"].to_list() # Get teh count and convert the value to list
    if len(res) > 0:
        res = res[0]
    else:
        res = -1

    connection.close()
    print(f"Count: {res}")
    return {"count": res}


@router.post("/mozhi/db/text/insert/annotations")
def insert_annotated_data(data: AnnotatedData):
    global connection
    formData: DBConnectionInfo = data.form_data
    if connection is None:
        connection = psycopg2.connect(host=formData.host,
                                      port=formData.port,
                                      database=formData.db_name,
                                      user=formData.user,
                                      password=formData.password)
    print("insert_annotated_data", data)
    # create a new cursor
    cur = connection.cursor()
    # execute the INSERT statement
    # TODO bound variables with kwargs
    sql_command = f"ALTER TABLE {formData.text_table_name} ADD COLUMN IF NOT EXISTS {formData.features_col_name} TEXT;"
    print(sql_command)
    cur.execute(sql_command)
    sql_command = f"ALTER TABLE {formData.text_table_name} ADD COLUMN IF NOT EXISTS {formData.labels_col_name} TEXT;"
    print(sql_command)
    cur.execute(sql_command)
    print(data)
    sql_command = f"UPDATE {formData.text_table_name} set {formData.features_col_name}=\'{data.tokens}\' where id={data.id};"
    print(sql_command)
    cur.execute(sql_command)
    sql_command = f"UPDATE {formData.text_table_name} set {formData.labels_col_name}=\'{data.labels}\' where id={data.id};"
    print(sql_command)
    cur.execute(sql_command)

    connection.commit()
    cur.close()
    print("<"*100)

# ----------------------------------------------------------------------------------------------------------------------


@router.post("/mozhi/db/image/create")
def insert_annotated_data(db_server: DBServer, experiment_name: str = Body(...)):
    global connection
    if connection is None:
        connection = psycopg2.connect(host=db_server.host,
                                      port=db_server.port,
                                      database=db_server.db_name,
                                      user=db_server.user,
                                      password=db_server.password)
    cur = connection.cursor()
    sql_command = f"create table if not exists {experiment_name}_image_annotations (" \
                  f"prefix text primary key, " \
                  f"bbox_json text, " \
                  f"ocr_text text, " \
                  f"ocr_text_bbox text, " \
                  f"features text," \
                  f"tags text)"
    cur.execute(sql_command)
    connection.commit()
    return {}


class BBoxJsonData(BaseModel):
    experiment_name: str
    prefix: str
    bbox_json: str
    ocr_text: str


@router.post("/mozhi/db/image/insert/bboxjson")
def insert_bbox_josn(data: BBoxJsonData):
    global connection
    cur = connection.cursor()
    sql_command = f"INSERT INTO {data.experiment_name}_image_annotations (prefix, bbox_json, ocr_text) " \
                  f"VALUES {data.prefix, data.bbox_json, data.ocr_text} ON CONFLICT (prefix) " \
                  f"DO UPDATE " \
                  f"SET prefix=EXCLUDED.prefix"
    print(sql_command)
    cur.execute(sql_command)
    connection.commit()
    return {}


def get_col(df, col_name):
    res = ""
    if df.size > 0:
        res = df[col_name].to_list()
        if len(res) > 0:
            res = res[0]
        else:
            res = ""
    return res


class ImageannotatedData(BaseModel):
    prefix: str
    experiment_name: str


@router.post("/mozhi/db/image/get/bboxjson") #TODO to GET ? axios doesn't have support to send data in body
def get_fabric_json(data: ImageannotatedData):
    global connection
    sql_command = f"SELECT * FROM \"{data.experiment_name}_image_annotations\" where prefix=\'{data.prefix}\';"

    df = pd.read_sql(sql_command, connection)
    res = {"bbox_json": get_col(df, "bbox_json"),
           "ocr_text": get_col(df, "ocr_text").replace("\\n", "\n"),
           "prefix": get_col(df, "prefix")}
    # print(res)
    return res
