import os
from dotenv import load_dotenv
from huggingface_hub import hf_hub_download

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAVE_DIR = os.path.join(BASE_DIR, "specxel", "models")
HF_TOKEN = os.getenv("HF_TOKEN")
HF_REPO_ID = os.getenv("HF_REPO_ID")

hf_hub_download(
    repo_id=HF_REPO_ID,
    filename='best_model.pth',
    local_dir=SAVE_DIR,
    token=HF_TOKEN
)

for f in os.listdir(SAVE_DIR):
    if not f.endswith(".pth"):
        path = os.path.join(SAVE_DIR, f)
        if os.path.isfile(path):
            os.remove(path)

cache_dir = os.path.join(SAVE_DIR, ".cache")
if os.path.isdir(cache_dir):
    import shutil
    shutil.rmtree(cache_dir)