import requests
from json.decoder import JSONDecodeError


response = requests.get("https://playground.learnqa.ru/api/hello", params={"name": "user"})

try:
    parsed_response_text = response.json()
    print(parsed_response_text["answer"])
except JSONDecodeError:
    print("Response is not JSON format")


response = requests.get("https://playground.learnqa.ru/api/get_text")

try:
    parsed_response_text = response.json()
    print(parsed_response_text["answer"])
except JSONDecodeError:
    print("Response is not JSON format")
