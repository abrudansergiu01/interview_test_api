import os

# Directory for the saved JSON data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# create the data directory if it doesn't exist
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# LM Studio API endpoint
LM_STUDIO_API_URL = "http://localhost:1234/v1/chat/completions"
API_BASE_URL = "http://127.0.0.1:8000"

# headers used for the LM Studio API req
HEADERS = {
    "Content-Type": "application/json"
}