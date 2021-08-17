from typing import List
from fastapi import File, UploadFile
from pydantic import BaseModel


class Text(BaseModel):
    text: str


class Words(BaseModel):
    words: List[str]


class ImageFile(BaseModel):
    file: UploadFile = File(...)


class ExtractedNER(BaseModel):
    text: str
    start: int
    end: int
    label: str
    type: str


class DBConnectionInfo(BaseModel):
    host: str
    port: str
    user: str
    password: str
    dbname: str
    # text_table_name: str = None
    # tag_table_name: str = None
    # text_col_name: str = None
    # features_col_name: str = None
    # labels_col_name: str = None
    # start_id: int = None

class DBServer(BaseModel):
    host: str
    port: str
    user: str
    password: str
    db_name: str

class Tokens(BaseModel):
    start: int
    end: int
    text: str
    type: str
    classId: str
    label: str


class AnnotatedData(BaseModel):
    id: int
    tokens: str
    labels: str
    features_col_name: str
    labels_col_name: str
    text_table_name: str
    connection_info: DBConnectionInfo


class StorageAuthentication(BaseModel):
    host: str
    port: str
    secretKey: str
    accessKey: str
