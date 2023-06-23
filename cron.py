import requests
import json

requests.post("http://127.0.0.1:5001/DataBase_update")
print(json.loads(requests.get("http://127.0.0.1:5001/DataBase_get_log?from=all").text))