from lib.my_requests import MyRequests as my_req
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserEdit(BaseCase, Assertions):
    def setup(self):
        # REGISTER
        registration_data = self.prepare_registration_data()
        response1 = my_req.post("/user", data=registration_data)

        self.assert_response_status_code(response1, 200)
        self.assert_json_has_key(response1, "id")

        self.email = registration_data["email"]
        self.first_name = registration_data["firstName"]
        self.password = registration_data["password"]
        self.user_id = self.get_json_value(response1, "id")
        self.username = registration_data["username"]

        # LOGIN
        login_data = {
            "email": self.email,
            "password": self.password
        }
        response2 = my_req.post("/user/login", data=login_data)

        self.auth_sid = self.get_cookie(response2, "auth_sid")
        self.token = self.get_header(response2, "x-csrf-token")

    def test_edit_just_created_user(self):
        # EDIT
        new_name = "Changed name"

        response3 = my_req.put(f"/user/{self.user_id}",
                               data={"firstName": new_name},
                               cookies={"auth_sid": self.auth_sid},
                               headers={"x-csrf-token": self.token}
                               )
        self.assert_response_status_code(response3, 200)

        # GET
        response4 = my_req.get(f"/user/{self.user_id}",
                               cookies={"auth_sid": self.auth_sid},
                               headers={"x-csrf-token": self.token}
                               )
        self.assert_response_status_code(response4, 200)
        self.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            f"Wrong name user after edit"
        )

    def test_edit_user_without_auth(self):
        # EDIT
        new_name = "Changed name"

        response3 = my_req.put(f"/user/{self.user_id}",
                               data={"firstName": new_name}
                               )
        self.assert_response_status_code(response3, 400)
        assert response3.text == "Auth token not supplied", \
            f"Unexpected response text '{response3.text}'"

    def test_edit_data_of_another_user(self):
        # REGISTER USER 2
        registration_data = self.prepare_registration_data()
        response1 = my_req.post("/user", data=registration_data)

        self.assert_response_status_code(response1, 200)
        self.assert_json_has_key(response1, "id")

        email_user2 = registration_data["email"]
        password_user2 = registration_data["password"]

        # LOGIN
        login_data = {
            "email": email_user2,
            "password": password_user2
        }
        response2 = my_req.post("/user/login", data=login_data)

        auth_sid_user2 = self.get_cookie(response2, "auth_sid")
        token_user2 = self.get_header(response2, "x-csrf-token")

        # EDIT USER1 BY AUTH USER2
        new_username = "Changed name"

        response3 = my_req.put(f"/user/{self.user_id}",
                               data={"username": new_username},
                               cookies={"auth_sid": auth_sid_user2},
                               headers={"x-csrf-token": token_user2}
                               )
        self.assert_response_status_code(response3, 200)
        assert response3.text is ""

        # GET
        response4 = my_req.get(f"/user/{self.user_id}",
                               cookies={"auth_sid": auth_sid_user2},
                               headers={"x-csrf-token": token_user2}
                               )
        actual_name = self.get_json_value(response4, "username")
        expected_absent_keys = ["firstName", "lastName", "email"]
        self.assert_response_status_code(response4, 200)
        self.assert_json_has_key(response4, "username")
        self.assert_json_value_by_name(response4, "username", self.username,
                                       f'Unexpected result user can change data of anther user.'
                                       f' Expected name is "{self.username}". But actual is "{actual_name}"')
        self.assert_json_doesnt_has_keys(response4, expected_absent_keys)

    def test_edit_user_email_without(self):
        # EDIT
        new_email = self.email.replace("@", "")

        response3 = my_req.put(f"/user/{self.user_id}",
                               data={"email": new_email},
                               cookies={"auth_sid": self.auth_sid},
                               headers={"x-csrf-token": self.token}
                               )
        self.assert_response_status_code(response3, 400)
        assert response3.text == "Invalid email format", \
            f"Unexpected response text '{response3.text}'"

    def test_edit_user_first_name_by_1(self):
        # EDIT
        new_first_name = "A"

        response3 = my_req.put(f"/user/{self.user_id}",
                               data={"firstName": new_first_name},
                               cookies={"auth_sid": self.auth_sid},
                               headers={"x-csrf-token": self.token}
                               )
        self.assert_response_status_code(response3, 400)
        assert response3.text == '{"error":"Too short value for field firstName"}', \
            f"Unexpected response text '{response3.text}'"
