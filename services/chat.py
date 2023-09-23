import os
ASTRA_DB_SECURE_BUNDLE_PATH = os.getenv('ASTRA_DB_SECURE_BUNDLE_PATH')
ASTRA_DB_APPLICATION_TOKEN = os.getenv('ASTRA_DB_APPLICATION_TOKEN')
ASTRA_DB_CLIENT_ID = os.getenv("ASTRA_DB_CLIENT_ID")
ASTRA_DB_CLIENT_SECRET = os.getenv("ASTRA_DB_CLIENT_SECRET")
ASTRA_DB_KEYSPACE = os.getenv("ASTRA_DB_KEYSPACE")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

from langchain.vectorstores.cassandra import Cassandra
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

cloud_config = {
    'secure_connect_bundle': ASTRA_DB_SECURE_BUNDLE_PATH
}

auth_provider = PlainTextAuthProvider(ASTRA_DB_CLIENT_ID, ASTRA_DB_CLIENT_SECRET)

cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
astraSession = cluster.connect()

llm = OpenAI(openai_api_key=OPENAI_API_KEY)
myEmbedding = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

myCassandraVStore = Cassandra(
    embedding=myEmbedding,
    session=astraSession,
    keyspace=ASTRA_DB_KEYSPACE,
    table_name="alfred_latest"
)


# print("\n Generating embeddings and storing in AstraDB")

# Example usage:
# pdf_path = "./aboutme.pdf"

# Split the PDF into text chunks
# chunks = split_pdf_into_text_chunks(pdf_path, max_tokens_per_chunk=1000)

# Add chunks to the vector store with rate limiting
# add_chunks_to_vector_store(chunks, myCassandraVStore)

vectorIndex = VectorStoreIndexWrapper(vectorstore=myCassandraVStore)

def chatService(query_text):
    if any(word in query_text.lower() for word in ["creator", "your creator", "created you?"]):
        answer = "My creator is EH Safin Ahmed. He created me as his butler Alfred Pennyworth"
    else:
        answer = vectorIndex.query(query_text, llm=llm).strip()
    
    return answer
