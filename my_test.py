import requests


# def test_phrase_len():
#     phrase = input("Set a phrase: ")
#     assert len(phrase) <= 15, f"Phrase is more than 15 characters, it is {len(phrase)} characters long"


def test_get_cookie():
    response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
    print('cookie>>>>>>  ' + str(response.cookies))
    cookie = response.cookies.get('HomeWork')
    assert cookie == 'hw_value'
