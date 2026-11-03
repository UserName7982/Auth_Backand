from langchain_community.vectorstores import LanceDB
from langchain_ollama import OllamaEmbeddings
import lancedb
import os
from ..config import configs
import pyarrow as pa

DB_PATH=os.path.join(configs.BASE_PATH, "lancedb") 

lancedb_conn=lancedb.connect(uri=DB_PATH)

embedding_function = OllamaEmbeddings(model="embeddinggemma:latest") 
dim = len(embedding_function.embed_query("test"))
doc_schema = pa.schema([
    ("chunk_id", pa.string()),               
    ("vector", pa.list_(pa.float32(), dim)),
    ("page_content", pa.string()),                
    ("source", pa.string()),
    ("chunk_index", pa.int32()),
    ("chunk_hash", pa.string()),
])

if "Documents" not in lancedb_conn.table_names():
    tbl=lancedb_conn.create_table("Documents", schema=doc_schema, data=[])
else:
    tbl=lancedb_conn.open_table("Documents")