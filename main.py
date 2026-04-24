import os
from dotenv import load_dotenv
from gen.gentext import run

load_dotenv()
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

run(NVIDIA_API_KEY)
# TODO FFPMEG VIDEO EDITING