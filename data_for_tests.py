import string
from datetime import datetime
import random


def generate_rnd_email():
    rnd_part = datetime.now().strftime("%m%d%Y%H%M%S%f")
    return f"{rnd_part}_@example.com"


def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


test_create_user_without_key_in_turn_test_data = [
    ({
         "username": "learnqa",
         "firstName": "learnqa",
         "lastName": "learnqa",
         "email": "vinkotov@example.com"
     }, "password"),
    ({
         "password": "123",
         "firstName": "learnqa",
         "lastName": "learnqa",
         "email": "vinkotov@example.com"
     }, "username"),
    ({
         "password": "123",
         "username": "learnqa",
         "lastName": "learnqa",
         "email": "vinkotov@example.com"
     }, "firstName"),
    ({
         "password": "123",
         "username": "learnqa",
         "firstName": "learnqa",
         "email": "vinkotov@example.com"
     }, "lastName"),
    ({
         "password": "123",
         "username": "learnqa",
         "firstName": "learnqa",
         "lastName": "learnqa",
     }, "email")
]

test_create_user_with_1_and_250_symbols_test_data = [
    ({
         "password": "123",
         "username": generate_random_string(1),
         "firstName": "learnqa",
         "lastName": "learnqa",
         "email": generate_rnd_email()
     }, "username_1"),
    ({
         "password": "123",
         "username": generate_random_string(250),
         "firstName": "learnqa",
         "lastName": "learnqa",
         "email": generate_rnd_email()
     }, "username_250"),
]
