import os, torch, sys, logging, pymongo
from dotenv import find_dotenv, dotenv_values
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import ServiceContext
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
from llama_index.core import StorageContext
from llama_index.core import SimpleDirectoryReader
from llama_index.core import VectorStoreIndex
from llama_index.readers.json import JSONReader


# Setup logging. To see more logging, set the level to DEBUG
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

""" Load Settings """

# Change system path to root direcotry
sys.path.insert(0, '../')

# _ = load_dotenv(find_dotenv()) # read local .env file
config = dotenv_values(find_dotenv())

ATLAS_URI = config.get('ATLAS_URI')

if not ATLAS_URI:
    raise Exception ("'ATLAS_URI' is not set.  Please set it above to continue...")
else:
    print("ATLAS_URI Connection string found:", ATLAS_URI)

# Define DB variables
DB_NAME = 'ava'
COLLECTION_NAME = 'sui'
INDEX_NAME = 'idx_embedding'

# LlamaIndex will download embeddings models as needed
# Set llamaindex cache dir to ../cache dir here (Default is system tmp)
# This way, we can easily see downloaded artifacts
os.environ['LLAMA_INDEX_CACHE_DIR'] = os.path.join(os.path.abspath('../'), 'cache')

mongodb_client = pymongo.MongoClient(ATLAS_URI)

""" Clear out collection """

database = mongodb_client[DB_NAME]
collection = database [COLLECTION_NAME]

doc_count = collection.count_documents (filter = {})
print (f"Document count before delete : {doc_count:,}")

result = collection.delete_many(filter= {})
print (f"Deleted docs : {result.deleted_count}")

""" Setup Embeddings """

embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
service_context = ServiceContext.from_defaults(embed_model=embed_model, llm=None)
vector_store = MongoDBAtlasVectorSearch(mongodb_client = mongodb_client,
                                 db_name = DB_NAME, collection_name = COLLECTION_NAME,
                                 index_name  = 'idx_embedding',
                                 )
storage_context = StorageContext.from_defaults(vector_store=vector_store)

""" Read PDF Documents """

pdf_data_dir = './ava/ava_backend/resources/pdfs'
pdf_docs = SimpleDirectoryReader(
        input_dir=pdf_data_dir
).load_data()

print (f"Loaded {len(pdf_docs)} chunks from '{pdf_data_dir}'")

# """ Read JSON Documents """

json_data_file = './ava/ava_backend/resources/all_json/output.json'
json_docs = JSONReader(levels_back=0).load_data(json_data_file)

print (f"Loaded {len(json_docs)} chunks from '{json_data_file}'")

""" Index the Documents and Store Them Into MongoDB Atlas """

pdf_index = VectorStoreIndex.from_documents(
    pdf_docs, 
    storage_context=storage_context,
    service_context=service_context,
)

json_index = VectorStoreIndex.from_documents(
    json_docs,
    storage_context=storage_context,
    service_context=service_context,
)
