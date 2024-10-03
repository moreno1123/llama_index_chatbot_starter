import logging

from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage
)
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def get_index():
    try:
        logger.info("Fetch loaded index")

        storage_context = StorageContext.from_defaults(
            persist_dir="data/storage/CA-2023"
        )
        index = load_index_from_storage(storage_context)

        index_loaded = True
    except:
        index_loaded = False

    # If not, create new one
    if not index_loaded:
        logger.info("Create new index")

        # Load data
        docs = SimpleDirectoryReader("data/CA").load_data()

        # Create index
        index = VectorStoreIndex.from_documents(docs)

        # Save
        index.storage_context.persist(persist_dir="data/storage/CA-2023")

    return index
