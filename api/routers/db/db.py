from fastapi import APIRouter, Body
from api.internal.json_models import DBDetails, AnnotatedData, DBServer
import pandas as pd
import psycopg2
import json
from pydantic import BaseModel
router = APIRouter()

connection = None


@router.post("/mozhi/db/text/get/tags")  # TODO make it as get/query
def get_table(data: DBDetails):
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
def get_row(row_id: int, data: DBDetails):
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
def get_total_rows(data: DBDetails):
    global connection
    if connection is None:
        connection = psycopg2.connect(host=data.host,
                                      port=data.port,
                                      database=data.db_name,
                                      user=data.user,
                                      password=data.password)
    sql_command = f"SELECT count(*) as count FROM \"{data.text_table_name}\";"

    df = pd.read_sql(sql_command, connection)
    res = df["count"].to_list() # Get teh count and convert the value to list
    if len(res) > 0:
        res = res[0]
    else:
        res = -1
    print(f"Count: {res}")
    return {"count": res}


@router.post("/mozhi/db/text/insert/annotations")
def insert_annotated_data(data: AnnotatedData):
    global connection
    formData: DBDetails = data.form_data
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
