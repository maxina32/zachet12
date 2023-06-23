import requests
import json

requests.post("http://127.0.0.1:5000/updateLogs")
print(json.loads(requests.get("http://127.0.0.1:5000/getEntries?from=all").text))