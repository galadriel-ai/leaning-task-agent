import hashlib
import json
import os
from typing import Dict

import requests


def execute(request: Dict, response: Dict):
    hashed_data = _hash_data(request, response)
    _make_request(request, response, hashed_data)


def _hash_data(request: Dict, response: Dict) -> str:
    combined_str = f"{_dump(request)}{_dump(response)}"
    return hashlib.sha256(combined_str.encode("utf-8")).digest().hex()


def _dump(data: Dict) -> str:
    return json.dumps(data, sort_keys=True)


def _make_request(request: Dict, response: Dict, hashed_data: str):
    # TODO: url = "https://api.galadriel.com/v1/verified/chat/log"
    url = "http://localhost:5000/v1/verified/chat/log"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + os.getenv("GALADRIEL_API_KEY"),
    }
    data = {
        "attestation": "TODO:",  # TODO
        "hash": hashed_data,
        "public_key": "TODO:",  # TODO
        "request": request,
        "response": response,
        "signature": "TODO:",  # TODO
    }
    result = requests.post(url, headers=headers, data=json.dumps(data))
    print("\nPOST verified chat log response:", result)


if __name__ == "__main__":
    execute({"hello": "world"}, {"goodbye": "world"})
