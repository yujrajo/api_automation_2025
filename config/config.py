import os
from dotenv import load_dotenv


api_data = {}
load_dotenv()
_api_token = os.getenv("TOKEN_ASANA")
url_base = os.getenv("URL_BASE")
workspace_gid = os.getenv("WORKSPACE_GID")
web_hook = os.getenv("WEB_HOOK")
influxdb_token = os.getenv("INFLUXDB_TOKEN")

headers = {"Authorization": f"Bearer {_api_token}"}
