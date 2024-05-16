import os, torch, sys, logging, pymongo
from dotenv import find_dotenv, dotenv_values
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import ServiceContext
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
from llama_index.core import StorageContext
from llama_index.core import SimpleDirectoryReader
from llama_index.core import VectorStoreIndex
from llama_index.llms.llama_api import LlamaAPI
from llama_index.core import Settings
from llama_index.core.llms import MockLLM
# from llama_index.llms.gemini import Gemini
# from llama_index.llms.huggingface import HuggingFaceLLM
# from llama_index.core import PromptTemplate


# Setup logging. To see more logging, set the level to DEBUG
# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.basicConfig(stream=sys.stdout, level=logging.INFO)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

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

""" Setup Embedding Model """

embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
Settings.embed_model = embed_model

""" Setup LLM """

api_key = config.get("LLAMA_API_KEY")
llm = LlamaAPI(api_key=api_key)
# llm = Gemini(api_key=os.getenv("GEMINI_API_KEY"))
# llm = MockLLM()
Settings.llm = llm
# service_context = ServiceContext.from_defaults(embed_model=embed_model, llm=llm)

""" Connect Llama-index and MongoDB Atlas """
vector_store = MongoDBAtlasVectorSearch(mongodb_client = mongodb_client,
                                 db_name = DB_NAME, collection_name = COLLECTION_NAME,
                                 index_name  = 'idx_embedding',
                                 )
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_vector_store(
    vector_store=vector_store,
    # service_context=service_context,
)

if __name__ == "__main__":
    from pprint import pprint
    from llama_index.core.memory import ChatMemoryBuffer
    
    memory = ChatMemoryBuffer.from_defaults()
    chat_engine = index.as_chat_engine(
        chat_mode="context",
        memory=memory,
        system_prompt=(
            """Your name is Ava and you are a sui blockchain expert. 
            You offer help regarding all sorts of issue related to 
            the sui blockchain and move programming language."""
        )
    )
    while True:
        query: str = str(input("\n\nQuery? "))
        response = chat_engine.chat(query)
        print(response)
    chat_engine.reset()