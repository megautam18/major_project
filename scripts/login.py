from huggingface_hub import login, whoami
from dotenv import load_dotenv
import os

load_dotenv()

login(os.getenv("hf_token"))

print(whoami())