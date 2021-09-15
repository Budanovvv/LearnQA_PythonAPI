import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect")
req_1 = response.history[0].url
req_2 = response.history[1].url
req_3 = response.history[2].url


print(f"First url {req_1}")
print(f"Second url {req_2}")
print(f"Finish url {req_3}")
