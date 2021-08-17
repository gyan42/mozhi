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
def create_db(connection_info: DBConnectionInfo, dbname: str) -> dict:
    """
    Creates a new Database with admin user credentials
    :param connection_info: Admin user credentials and connection address
    :param dbname: Name of the new Database
    :return: {"status" : "Success/Failed"}
    :rtype: dict
    """
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
    """
    Uploads the Conll based data to Database
    :param connection_info: Database connection info
    :param files:
    :return:
    """
    try:
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
        return {"status": "Success"}
    except Exception as e:
        print(e)
        return {"status": "Failed"}


@router.post("/mozhi/db/text/get/counts")
def get_total_rows(connection_info: DBConnectionInfo, text_table_name: str):
    """
    Get total number of rows
    :param connection_info: DB admin user credentials
    :param text_table_name:
    :return:
    """
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
        res = 0

    connection.close()
    print(f"Count: {res}")
    return {"count": res}

@router.post("/mozhi/db/text/get/dblist")
def get_dblist(connection_info: DBConnectionInfo):
    """
    Returns list of databases
    :param connection_info: DB admin user credentials
    :return:
    """
    connection = psycopg2.connect(host=connection_info.host,
                                  port=connection_info.port,
                                  database=connection_info.dbname,
                                  user=connection_info.user,
                                  password=connection_info.password)
    df = pd.read_sql("SELECT datname FROM pg_database WHERE datistemplate = false;", connection)
    dblist = df['datname'].to_list()
    return {"dblist": dblist}


@router.post("/mozhi/db/text/get/tablelist")
def get_tablelist(connection_info: DBConnectionInfo):
    """
    Returns list of tables for given connection info
    :param connection_info: DB admin user credentials
    :return:
    """
    connection = psycopg2.connect(host=connection_info.host,
                                  port=connection_info.port,
                                  database=connection_info.dbname,
                                  user=connection_info.user,
                                  password=connection_info.password)
    df = pd.read_sql("SELECT table_name FROM information_schema.tables WHERE table_type = 'BASE TABLE' AND table_schema = 'public' ORDER BY table_type, table_name;",
                     connection)
    table_list = df['table_name'].to_list()
    return {"tablelist": table_list}


@router.post("/mozhi/db/text/get/tags")  # TODO make it as get/query
def get_tags(connection_info: DBConnectionInfo, tag_table_name: str):
    """
    Returns set of NER tags in the given tag table
    :param connection_info:
    :param tag_table_name:
    :return:
    """
    connection = psycopg2.connect(host=connection_info.host,
                                  port=connection_info.port,
                                  database=connection_info.dbname,
                                  user=connection_info.user,
                                  password=connection_info.password)
    sql_command = f"SELECT * FROM \"{tag_table_name}\";"

    df = pd.read_sql(sql_command, connection)
    tags = df["name"].to_list()
    return {"tags": tags}


@router.post("/mozhi/db/text/get/row")
def get_row(table_name: str, row_id: int, connection_info: DBConnectionInfo):
    """
    Returns a row from text table
    :param table_name:
    :param row_id:
    :param connection_info:
    :return: {"text":"", "features": "", "labels": ""}
    """
    connection = psycopg2.connect(host=connection_info.host,
                                  port=connection_info.port,
                                  database=connection_info.dbname,
                                  user=connection_info.user,
                                  password=connection_info.password)
    sql_command = f"SELECT * FROM \"{table_name}\" where id = {row_id};"
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


@router.post("/mozhi/db/text/insert/annotations")
def insert_annotated_data(data: AnnotatedData):
    connection_info: DBConnectionInfo = data.connection_info

    connection = psycopg2.connect(host=connection_info.host,
                                  port=connection_info.port,
                                  database=connection_info.dbname,
                                  user=connection_info.user,
                                  password=connection_info.password)
    print("insert_annotated_data", data)
    # create a new cursor
    cur = connection.cursor()
    # execute the INSERT statement
    # TODO bound variables with kwargs
    sql_command = f"ALTER TABLE {data.text_table_name} ADD COLUMN IF NOT EXISTS {data.features_col_name} TEXT;"
    print(sql_command)
    cur.execute(sql_command)
    sql_command = f"ALTER TABLE {data.text_table_name} ADD COLUMN IF NOT EXISTS {data.labels_col_name} TEXT;"
    print(sql_command)
    cur.execute(sql_command)
    print(data)
    sql_command = f"UPDATE {data.text_table_name} set {data.features_col_name}=\'{data.tokens}\' where id={data.id};"
    print(sql_command)
    cur.execute(sql_command)
    sql_command = f"UPDATE {data.text_table_name} set {data.labels_col_name}=\'{data.labels}\' where id={data.id};"
    print(sql_command)
    cur.execute(sql_command)

    connection.commit()
    cur.close()
    print("<"*100)


# ------------------------------------------------------------------------------------------------------------------------


@router.post("/mozhi/db/image/create/table")
def create_image_annotations_table(db_connection_info: DBConnectionInfo, experiment_name: str = Body(...)):

    connection = psycopg2.connect(host=db_connection_info.host,
                                  port=db_connection_info.port,
                                  database=db_connection_info.dbname,
                                  user=db_connection_info.user,
                                  password=db_connection_info.password)
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
def insert_bbox_josn(db_connection_info: DBConnectionInfo,
                     experiment_name: str = Body(...),
                     prefix: str = Body(...),
                     bbox_json: str = Body(...),
                     ocr_text: str = Body(...)):
    connection = psycopg2.connect(host=db_connection_info.host,
                                  port=db_connection_info.port,
                                  database=db_connection_info.dbname,
                                  user=db_connection_info.user,
                                  password=db_connection_info.password)
    cur = connection.cursor()
    sql_command = f"INSERT INTO {experiment_name}_image_annotations (prefix, bbox_json, ocr_text) " \
                  f"VALUES {prefix, bbox_json, ocr_text} ON CONFLICT (prefix) " \
                  f"DO UPDATE " \
                  f"SET prefix=EXCLUDED.prefix"
    print(sql_command)
    cur.execute(sql_command)
    connection.commit()
    return {"status": "Success"}


def get_col(df, col_name):
    res = ""
    if df.size > 0:
        res = df[col_name].to_list()
        if len(res) > 0:
            res = res[0]
        else:
            res = ""
    return res


@router.post("/mozhi/db/image/get/bboxjson") #TODO to GET ? axios doesn't have support to send data in body
def get_fabric_json(db_connection_info: DBConnectionInfo, prefix: str = Body(...), experiment_name: str = Body(...)):
    connection = psycopg2.connect(host=db_connection_info.host,
                                  port=db_connection_info.port,
                                  database=db_connection_info.dbname,
                                  user=db_connection_info.user,
                                  password=db_connection_info.password)
    sql_command = f"SELECT * FROM \"{experiment_name}_image_annotations\" where prefix=\'{prefix}\';"

    df = pd.read_sql(sql_command, connection)
    res = {"bbox_json": get_col(df, "bbox_json"),
           "ocr_text": get_col(df, "ocr_text").replace("\\n", "\n"),
           "prefix": get_col(df, "prefix")}
    print(res)
    return res
