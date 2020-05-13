import os 
from dotenv import load_dotenv

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE_PATH = os.path.join(ROOT_DIR,'.env')

load_dotenv(dotenv_path=ENV_FILE_PATH)

SECRET_KEY = os.getenv("tiingo_API_KEY")

# print(os.path.dirname(os.path.abspath(__file__)))
# print(os.path.abspath(__file__))
# print(ROOT_DIR)
print(ENV_FILE_PATH)

