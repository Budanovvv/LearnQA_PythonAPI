from lib.my_requests import MyRequests as my_req
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserGet(BaseCase, Assertions):

    def setup(self):
        response1 = my_req.post("/user/login",
                                data={
                                    "email": "vinkotov@example.com",
                                    "password": "1234",
                                })
        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response1, "user_id")
        self.assert_response_status_code(response1, 200)

    def test_get_user_get_details_not_auth(self):
        response = my_req.get("/user/2")

        expected_absent_keys = ["firstName", "lastName", "email"]
        self.assert_response_status_code(response, 200)
        self.assert_json_has_key(response, "username")
        self.assert_json_doesnt_has_keys(response, expected_absent_keys)

    def test_get_user_get_details_auth_is_same_user(self):
        response2 = my_req.get(f"/user/{self.user_id_from_auth_method}",
                               cookies={"auth_sid": self.auth_sid},
                               headers={"x-csrf-token": self.token}
                               )

        expected_keys = ["username", "firstName", "lastName", "email"]
        self.assert_response_status_code(response2, 200)
        self.assert_json_has_keys(response2, expected_keys)

    def test_auth_user_try_to_get_details_another_user(self):
        response2 = my_req.get(f"/user/{self.user_id_from_auth_method + 1}",
                               cookies={"auth_sid": self.auth_sid},
                               headers={"x-csrf-token": self.token}
                               )
        self.assert_response_status_code(response2, 404)
        assert response2.text == 'User not found', f"Unexpected response text '{response2.text}'"
