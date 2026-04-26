import logging

from sentence_transformers import SentenceTransformer
import chromadb
from starlette.responses import Response, PlainTextResponse
from http import HTTPStatus
import json

from .db_operations import XmlAndDatabaseOperations

# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Log to console
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

# Also log to a file
file_handler = logging.FileHandler("./logs/chromadb-operations.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class ChromaDatabaseOperations:

    def __init__(self):
        xmlAndDatabaseOperations = XmlAndDatabaseOperations()

        # Load embedding model
        sentence_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

        # Create Chroma client + collection
        client = chromadb.Client()
        chroma_collection = client.create_collection(name="sentences")

        self.xmlAndDatabaseOperations = xmlAndDatabaseOperations
        self.sentence_model = sentence_model
        self.chroma_collection = chroma_collection


    def ingest_into_chroma(self, list_of_ingest_pks: list, list_of_ingest_sentence_data: list) -> Response:
        """
        Generate embeddings from a list of strings (PRODUCT TABLE ALL ROWS, name and description)

        :param list_of_ingest_pks: list<ids,pk>
        :param list_of_ingest_sentence_data: list<str> productName and productDescription
        :return: Http response with the status (single string)
        """
        # Generate embeddings
        embeddings = self.sentence_model.encode(list_of_ingest_sentence_data).tolist()

        # Add to Chroma
        self.chroma_collection.add(
            documents=list_of_ingest_sentence_data,
            embeddings=embeddings,
            ids=list_of_ingest_pks,
        )

        return PlainTextResponse("Did correctly ingest into chroma db", status_code=200)



    def query_chroma_retrieve_from_mariadb(self, chroma_query_token: str) -> Response:
        """
        From the web-page, user inputs a sentence (search term that we need to match - via chroma)
        delegate query to chroma db. returns PK,IDS which we use to retrieve PRODUCT data from MariaDb

        :param chroma_query_token: sentence search term
        :return: Http response with the json string (fail status or list<PRODUCT>)
        """
        if chroma_query_token is None or len(chroma_query_token) <= 0:
            return Response(status_code=HTTPStatus.OK, content="Received http path variable chroma-query-token is none or empty. cannot process. exit")

        # Query
        chroma_model_query_emb = self.sentence_model.encode([chroma_query_token]).tolist()

        chroma_results = self.chroma_collection.query(
            query_embeddings=chroma_model_query_emb,
            n_results=2
        )

        if chroma_results is None:
            return Response(status_code=HTTPStatus.OK, content="No data was returned in chroma-results. cannot process. exit")

        logging.debug("T1")
        logging.debug(chroma_results)
        ids = chroma_results["ids"]
        if ids is None or len(ids) <= 0:
            return Response(status_code=HTTPStatus.OK, content="Chroma-results ids was null or empty. cannot process. exit")

        logging.debug("ids_type={}, ids_value={} len(ids)={}".format(type(ids), ids,len(ids),))
        id_ids = ids[0]
        if id_ids is None or len(id_ids) <= 0:
            return Response(status_code=HTTPStatus.OK, content="Chroma-results id_ids was null or empty. cannot process. exit")

        logging.debug("id_ids_type={}, id_ids_value={}".format(type(id_ids),id_ids,))
        logging.debug("T13")

        list_chroma_retrieve_maria = self.xmlAndDatabaseOperations.read_chroma_results_retrieve_and_validate_with_dtd(id_ids)

        if list_chroma_retrieve_maria is None or len(list_chroma_retrieve_maria) <= 0:
            return Response(status_code=HTTPStatus.OK, content="Did not retrieve any data after chroma. cannot process. exit")
        else:
            json_chroma_string = json.dumps(list_chroma_retrieve_maria)
            return Response(status_code=HTTPStatus.OK, content=json_chroma_string, media_type="application/json")
