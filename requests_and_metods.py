import requests
from json.decoder import JSONDecodeError


response_methods = ["GET", "POST", "PUT", "DELETE", "HEAD", ""]
url = "https://playground.learnqa.ru/ajax/api/compare_query_type"


def check_response(response):
    try:
        if response.json()["success"]:
            print(f"{response.request.method}, data 'method' {resp_method} -> {response.text}")
    except JSONDecodeError:
        if resp_method == "":
            print(f"{response.request.method}, 'method is absent or empty' -> {response.text}")
        else:
            print(f"{response.request.method}, 'method' {resp_method} -> {response.text}")


print("<<<<<<<<<<<<Метод GET>>>>>>>>>>>>>>")
for resp_method in response_methods:
    response = requests.get(url, params={"method": resp_method})
    check_response(response)

for resp_method in response_methods:
    response = requests.get(url, data={"method": resp_method})
    check_response(response)

response = requests.get(url)
check_response(response)

print("<<<<<<<<<<<<Метод POST>>>>>>>>>>>>>>")
for resp_method in response_methods:
    response = requests.post(url, data={"method": resp_method})
    check_response(response)

for resp_method in response_methods:
    response = requests.post(url, params={"method": resp_method})
    check_response(response)

response = requests.post(url)
check_response(response)

print("<<<<<<<<<<<<Метод PUT>>>>>>>>>>>>>>")
for resp_method in response_methods:
    response = requests.put(url, data={"method": resp_method})
    check_response(response)

for resp_method in response_methods:
    response = requests.put(url, params={"method": resp_method})
    check_response(response)

response = requests.put(url)
check_response(response)

print("<<<<<<<<<<<<Метод DELETE>>>>>>>>>>>>>>")
for resp_method in response_methods:
    response = requests.delete(url, data={"method": resp_method})
    check_response(response)

for resp_method in response_methods:
    response = requests.delete(url, params={"method": resp_method})
    check_response(response)

response = requests.delete(url)
check_response(response)
