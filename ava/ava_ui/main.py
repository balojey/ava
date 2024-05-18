import streamlit as st
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
from llama_index.llms.gemini import Gemini
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.core import PromptTemplate
from transformers import AutoTokenizer, AutoModelForCausalLM
from llama_index.core.memory import ChatMemoryBuffer


st.title("Ava - Sui/Move Expert")

# Load Settings

# Change system path to root direcotry
sys.path.insert(0, '../')

# _ = load_dotenv(find_dotenv()) # read local .env file
config = dotenv_values(find_dotenv())

ATLAS_URI = config.get('ATLAS_URI') or st.secrets["ATLAS_URI"]

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

# Setup Embedding Model

embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
Settings.embed_model = embed_model

# Setup LLM

llm = LlamaAPI(api_key=config.get("LLAMA_API_KEY") or st.secrets["LLAMA_API_KEY"])
# llm = Gemini(api_key=config.get("GEMINI_API_KEY"), model_name="models/gemini-pro")
# llm = MockLLM()
# system_prompt = """Your name is Ava and you are a sui blockchain expert. 
#             You offer help regarding all sorts of issue related to 
#             the sui blockchain and move programming language."""
# messages = [
#     {
#         "role": "system",
#         "content": """Your name is Ava and you are a sui blockchain expert. 
#             You offer help regarding all sorts of issue related to 
#             the sui blockchain and move programming language.""",
#     },
#     {"role": "user", "content": "How is the move programming language different from other smart contract programming language"},
# ]
# checkpoint = "StabilityAI/stablelm-tuned-alpha-3b"
# query_wrapper_prompt = PromptTemplate("<|USER|>{query_str}<|ASSISTANT|>")
# model = AutoModelForCausalLM.from_pretrained(checkpoint)  # You may want to use bfloat16 and/or move to GPU here
# tokenizer = AutoTokenizer.from_pretrained(checkpoint, padding_side="left")
# model.generation_config.pad_token_id = tokenizer.pad_token_id
# tokenized_chat = tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, return_tensors="pt")
# print("tokenizer: >>>>> : ", tokenizer.decode(tokenized_chat[0]))

# llm = HuggingFaceLLM(
#     context_window=4096,
#     max_new_tokens=256,
#     generate_kwargs={"do_sample": True},
#     system_prompt=system_prompt,
#     query_wrapper_prompt=query_wrapper_prompt,
#     # tokenizer_name=checkpoint,
#     # model_name=checkpoint,
#     device_map="auto",
#     stopping_ids=[50278, 50279, 50277, 1, 0],
#     tokenizer_kwargs={"max_length": 4096},
#     tokenizer=tokenizer,
#     model=model,
#     # uncomment this if using CUDA to reduce memory usage
#     # model_kwargs={"torch_dtype": torch.float16}
# )
Settings.llm = llm
# service_context = ServiceContext.from_defaults(embed_model=embed_model, llm=llm)

# Connect Llama-index and MongoDB Atlas
vector_store = MongoDBAtlasVectorSearch(mongodb_client = mongodb_client,
                                 db_name = DB_NAME, collection_name = COLLECTION_NAME,
                                 index_name  = 'idx_embedding',
                                 )
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_vector_store(
    vector_store=vector_store,
    # service_context=service_context,
)

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

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = memory.get_all()

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = chat_engine.chat(prompt)
        response.is_dummy_stream = True
        st.write_stream(response.response_gen)
    st.session_state.messages.append({"role": "assistant", "content": response})