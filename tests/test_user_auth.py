import pytest
from lib.my_requests import MyRequests as my_req
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserAuth(BaseCase, Assertions):
    exclude_params = [
        "no_cookie",
        "no_header"
    ]

    def setup(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }
        response1 = my_req.post("/user/login", data=data)

        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response1, "user_id")

    def test_user_auth(self):
        response2 = my_req.get("/user/auth",
                                 headers={"x-csrf-token": self.token},
                                 cookies={"auth_sid": self.auth_sid}
                                 )

        self.assert_json_value_by_name(
            response2,
            "user_id",
            self.user_id_from_auth_method,
            "User id from auth method is nor equal user id from check method"
        )

    @pytest.mark.parametrize("condition", exclude_params)
    def test_negative_check(self, condition):
        if condition == "no_cookie":
            response2 = my_req.get(
                "/user/auth",
                headers={"x-csrf-token": self.token})
        else:
            response2 = my_req.get(
                "/user/auth",
                cookies={"auth_sid": self.auth_sid})

        self.assert_json_value_by_name(response2, "user_id", 0, f"User is authorised by condition - {condition}")
