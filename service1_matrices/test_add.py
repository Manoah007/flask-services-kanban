import urllib.request
import json

url = "http://localhost:5001/matrices/add"

data = {
    "A": [[1, 2], [3, 4]],
    "B": [[5, 6], [7, 8]]
}

req = urllib.request.Request(
    url,
    data=json.dumps(data).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST"
)

with urllib.request.urlopen(req) as response:
    result = json.loads(response.read().decode("utf-8"))
    print(result)