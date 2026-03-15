import os
from dotenv import load_dotenv
from huggingface_hub import hf_hub_download

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_DIR = os.path.join(BASE_DIR, "models")
HF_TOKEN = os.getenv("HF_TOKEN")
HF_REPO_ID = os.getenv("HF_REPO_ID")

hf_hub_download(
    repo_id=HF_REPO_ID,
    filename='best_model.pth',
    local_dir=SAVE_DIR,
    token=HF_TOKEN
)
