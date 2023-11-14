
from dotenv import load_dotenv
import os
from chromadb.config import Settings

#load_dotenv('config.env')

# Define the folder for storing database
PERSIST_DIRECTORY = "db"
#os.environ.get("TARGET_SOURCE_CHUNKS")
print(PERSIST_DIRECTORY)
if PERSIST_DIRECTORY is None:
    raise Exception("Please set the PERSIST_DIRECTORY environment variable")

# Define the Chroma settings
CHROMA_SETTINGS = Settings(
        persist_directory="db",
      anonymized_telemetry=False
)
