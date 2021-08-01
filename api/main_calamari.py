"""
https://fastapi.tiangolo.com/tutorial/cors/

"""

import uvicorn
from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

# from api.routers.nlp import nlp
# from api.routers.db import db
# from api.routers.ner.model import spacy_ner
# from api.routers.ner.model import transformers_ner
from api.routers.ocr.calamari import calamari
# from api.routers.ocr.tesseract import tesseract
# from api.routers.storage import minio

app = FastAPI(
    # root_path="/api/v1",
    title="Mozhi API Service",
    description="""Visit http://0.0.0.0:8089/docs for the API interface.""",
    version="0.0.1"
)

# app.include_router(nlp.router)
# app.include_router(db.router)
app.include_router(calamari.router)
# app.include_router(tesseract.router)
# app.include_router(spacy_ner.router)
# app.include_router(transformers_ner.router)
# app.include_router(minio.router)

ALLOWED_ORIGINS = ["*"]

app.add_middleware(GZipMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root(request: Request):
    return {"message": "Hello, Welcome to Mozhi API.", "root_path": request.scope.get("root_path")}


@app.get("/hw")
def read_main(request: Request):
    return {"message": "Hello World! Mozhi backend responds as expected.", "root_path": request.scope.get("root_path")}


# https://github.com/tiangolo/fastapi/issues/1663
def check_routes(request: Request):
    # Using FastAPI instance
    url_list = [
        route.path
        for route in request.app.routes
        if "rest_of_path" not in route.path
    ]
    # Dump fix for /mozhi/db/text/table/
    if request.url.path not in url_list and '/mozhi/db/text/table/' not in request.url.path:
        return JSONResponse({"detail": request.url.path + " Not Found"}, status.HTTP_404_NOT_FOUND)


# Handle CORS preflight requests
@app.options("/{rest_of_path:path}")
async def preflight_handler(request: Request, rest_of_path: str) -> Response:
    response = check_routes(request)
    if response:
        return response

    response = Response(
        content="OK",
        media_type="text/plain",
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        },
    )
    return response


# Add CORS headers
@app.middleware("http")
async def add_cors_header(request: Request, call_next):
    response = check_routes(request)
    if response:
        return response

    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8089, reload=True)
