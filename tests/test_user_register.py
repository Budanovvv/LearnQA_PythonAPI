from datetime import datetime
from pprint import pprint

import requests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
import data_for_tests as dft


class TestUserAuth(BaseCase, Assertions):

    def setup(self):
        rnd_part = datetime.now().strftime("%m%d%Y%H%M%S")
        self.email = f"{rnd_part}_@example.com"

    def test_create_user_successfully(self):
        data = {
            "password": "123",
            "username": "learnqa",
            "firstName": "learnqa",
            "lastName": "learnqa",
            "email": self.email
        }

        response = requests.post(
            "https://playground.learnqa.ru/api/user", data=data)

        Assertions.assert_response_status_code(response, 200)
        Assertions.assert_json_by_name(response, "id")

    def test_create_user_with_existing_email(self):
        email = "vinkotov@example.com"
        data = {
            "password": "123",
            "username": "learnqa",
            "firstName": "learnqa",
            "lastName": "learnqa",
            "email": email
        }

        response = requests.post(
            "https://playground.learnqa.ru/api/user", data=data)

        Assertions.assert_response_status_code(response, 400)
        assert response.text == f"Users with email '{email}' already exists",\
            f"Unexpected response text '{response.text}'"

    def test_create_user_with_incorrect_email(self):
        email = "vinkotovexample.com"
        data = {
            "password": "123",
            "username": "learnqa",
            "firstName": "learnqa",
            "lastName": "learnqa",
            "email": email
        }

        response = requests.post(
            "https://playground.learnqa.ru/api/user", data=data)

        Assertions.assert_response_status_code(response, 400)
        assert response.text == "Invalid email format",\
            f"Unexpected response text '{response.text}'"

    @pytest.mark.parametrize("json_data, absent_key", dft.test_create_user_without_key_in_turn_test_data)
    def test_create_user_without_key_in_turn(self, json_data, absent_key):

        response = requests.post(
            "https://playground.learnqa.ru/api/user", data=json_data)

        Assertions.assert_response_status_code(response, 400)
        assert response.text == f"The following required params are missed: {absent_key}",\
            f"Unexpected response text '{response.text}'"

    @pytest.mark.parametrize("json_data, condition", dft.test_create_user_with_1_and_250_symbols_test_data)
    def test_create_user_with_1_and_250_symbols(self, json_data, condition):

        response = requests.post(
            "https://playground.learnqa.ru/api/user", data=json_data)

        if condition == "username_1":
            Assertions.assert_response_status_code(response, 400)
            assert response.text == f"The value of 'username' field is too short", \
                f"Unexpected response text '{response.text}'"
        elif condition == "username_250":
            Assertions.assert_response_status_code(response, 200)
            Assertions.assert_json_by_name(response, "id")
