from http import HTTPStatus
from fastapi import FastAPI
from starlette.responses import Response, PlainTextResponse
from pkg_resources import resource_filename
import json
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

from .sql_dll_functions.db_operations import XmlAndDatabaseOperations
from .sql_dll_functions.chromadb_operations import ChromaDatabaseOperations

xmlAndDatabaseOperations = XmlAndDatabaseOperations()
chromaDatabaseOperations = ChromaDatabaseOperations()

app = FastAPI(title="WebAppFirstIteration", version="1.0")

app.mount("/first-webapp-demo",
    StaticFiles(directory=resource_filename(__name__, 'static-content'), html = True),
    name="static-content")

@app.get("/healthcheck")
async def health() -> Response:
    return Response(status_code=HTTPStatus.OK, content="Hello Bill")

@app.get("/")
async def root():
    return FileResponse("static-content/NoContentHere.html")

@app.get("/create_tables", response_class=PlainTextResponse)
def create_tables() -> Response:
    boolean_status = xmlAndDatabaseOperations.read_create_and_validate_with_dtd()
    return PlainTextResponse(str(boolean_status), status_code=200)

@app.get("/insert_into_tables", response_class=PlainTextResponse)
def insert_into_tables() -> Response:
    boolean_status = xmlAndDatabaseOperations.read_insert_and_validate_with_dtd()
    return PlainTextResponse(str(boolean_status), status_code=200)

@app.get("/add_constraints_tables", response_class=PlainTextResponse)
def add_constraints_tables() -> Response:
    boolean_status = xmlAndDatabaseOperations.read_foreign_key_and_validate_with_dtd()
    return PlainTextResponse(str(boolean_status), status_code=200)

@app.get("/select_from_tables")
def select_from_tables() -> Response:
    list_ret = xmlAndDatabaseOperations.read_select_and_validate_with_dtd()
    json_string = json.dumps(list_ret)
    return Response(status_code=HTTPStatus.OK, content=json_string, media_type="application/json")

@app.get("/ingest_into_chroma", response_class=PlainTextResponse)
def select_then_ingest() -> Response:
    list_ingest_ret = xmlAndDatabaseOperations.read_ingest_to_chroma_with_dtd()
    if list_ingest_ret is None or len(list_ingest_ret) <= 0:
        return Response(status_code=HTTPStatus.OK, content="No data was returned. cannot process. exit")
    list_of_ingest_pks = []
    list_of_ingest_sentence_data = []
    for obj in list_ingest_ret:
        pk = obj["pk"]
        sentence_data = obj["sentenceData"]
        list_of_ingest_pks.append(pk)
        list_of_ingest_sentence_data.append(sentence_data)

    return chromaDatabaseOperations.ingest_into_chroma(list_of_ingest_pks, list_of_ingest_sentence_data)

@app.get("/query_chroma_retrieve_from_maria/{chroma_query_token}")
def query_chroma_retrieve_from_maria(chroma_query_token: str) -> Response:

    return chromaDatabaseOperations.query_chroma_retrieve_from_mariadb(chroma_query_token)

@app.get("/drop_tables", response_class=PlainTextResponse)
def drop_tables() -> Response:
    boolean_status = xmlAndDatabaseOperations.read_drop_and_validate_with_dtd()
    return PlainTextResponse(str(boolean_status), status_code=200)
