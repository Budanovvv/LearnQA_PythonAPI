from lib.my_requests import MyRequests as my_req
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
import data_for_tests as dft


class TestUserAuth(BaseCase, Assertions):

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = my_req.post(
            "/user", data=data)

        Assertions.assert_response_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        data = self.prepare_registration_data("vinkotov@example.com")
        email = data["email"]

        response = my_req.post(
            "/user", data=data)

        Assertions.assert_response_status_code(response, 400)
        assert response.text == f"Users with email '{email}' already exists",\
            f"Unexpected response text '{response.text}'"

    def test_create_user_with_incorrect_email(self):
        data = self.prepare_registration_data("vinkotovexample.com")

        response = my_req.post(
            "/user", data=data)

        Assertions.assert_response_status_code(response, 400)
        assert response.text == "Invalid email format",\
            f"Unexpected response text '{response.text}'"

    @pytest.mark.parametrize("json_data, absent_key", dft.test_create_user_without_key_in_turn_test_data)
    def test_create_user_without_key_in_turn(self, json_data, absent_key):

        response = my_req.post(
            "/user", data=json_data)

        Assertions.assert_response_status_code(response, 400)
        assert response.text == f"The following required params are missed: {absent_key}",\
            f"Unexpected response text '{response.text}'"

    @pytest.mark.parametrize("json_data, condition", dft.test_create_user_with_1_and_250_symbols_test_data)
    def test_create_user_with_1_and_250_symbols(self, json_data, condition):

        response = my_req.post(
            "/user", data=json_data)

        if condition == "username_1":
            Assertions.assert_response_status_code(response, 400)
            assert response.text == f"The value of 'username' field is too short", \
                f"Unexpected response text '{response.text}'"
            print(response.content)
        elif condition == "username_250":
            print(response.content)
            Assertions.assert_response_status_code(response, 200)
            Assertions.assert_json_has_key(response, "id")
