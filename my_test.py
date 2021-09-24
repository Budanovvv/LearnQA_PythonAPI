

import requests


def test_phrase_maxlen_15():
    phrase = input("Set a phrase: ")
    assert len(phrase) <= 15, f"Phrase is more than 15 characters, it is {len(phrase)} characters long"


def test_get_cookie():
    response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
    print('cookie>>>>>>  ' + str(response.cookies))
    cookie_name = 'HomeWork'
    assert cookie_name in response.cookies, f"There is no cookie {cookie_name} in response"
    cookie_value = response.cookies.get(cookie_name)
    assert cookie_value == 'hw_value', f"Cookie have wrong value - {cookie_value}"


def test_get_header():
    response = requests.get("https://playground.learnqa.ru/api/homework_header")
    print('headers>>>>>>  ' + str(response.headers))
    header_name = 'x-secret-homework-header'
    assert header_name in response.headers, f"There is no header {header_name} in response"
    header_value = response.headers.get(header_name)
    assert header_value == 'Some secret value', f"Cookie have wrong value - {header_value}"