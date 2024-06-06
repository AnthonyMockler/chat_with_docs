import openai
import llama_index
from llama_index.llms.openai import OpenAI
try:
  from llama_index import VectorStoreIndex, ServiceContext, Document, SimpleDirectoryReader
except ImportError:
  from llama_index.core import VectorStoreIndex, ServiceContext, Document, SimpleDirectoryReader

from azure.storage.blob import BlobServiceClient
from io import BytesIO

from llama_index.core.extractors import (
    TitleExtractor,
    QuestionsAnsweredExtractor,
)
from llama_index.core.node_parser import TokenTextSplitter
import streamlit as st

azure_storage_account_name = st.secrets.azure_storage_account_name
azure_storage_account_key = st.secrets.azure_storage_account_key
container_name = st.secrets.container_name
connection_string_blob =st.secrets.connection_string_blob

blob_service_client = BlobServiceClient.from_connection_string(f"DefaultEndpointsProtocol=https;AccountName={azure_storage_account_name};AccountKey={azure_storage_account_key}")



def list_all_containers():
    container_list = list()
    containers = blob_service_client.list_containers()
    for container in containers:
        container_list.append(container.name)
    return container_list


def list_all_files(container_name):
    blob_list = blob_service_client.get_container_client(container_name).list_blobs()
    blob_list_display = []
    for blob in blob_list:
        blob_list_display.append(blob.name)
    return blob_list_display


def upload_to_azure_storage(file):
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file.name)
    blob_client.upload_blob(file)
