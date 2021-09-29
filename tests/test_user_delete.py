from lib.my_requests import MyRequests as my_req
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserDelete(BaseCase, Assertions):
    def login(self, email=None, password=None):
        if password is None and email is None:
            # REGISTER
            registration_data = self.prepare_registration_data()
            response1 = my_req.post("/user", data=registration_data)

            self.email = registration_data["email"]
            self.password = registration_data["password"]
            self.username = registration_data["username"]

            self.assert_response_status_code(response1, 200)
            self.assert_json_has_key(response1, "id")

            # LOGIN
            login_data = {
                "email": self.email,
                "password": self.password
            }
            response2 = my_req.post("/user/login", data=login_data)
        else:
            # LOGIN
            login_data = {
                "email": email,
                "password": password
            }

            response2 = my_req.post("/user/login", data=login_data)

        self.assert_response_status_code(response2, 200)
        self.auth_sid = self.get_cookie(response2, "auth_sid")
        self.token = self.get_header(response2, "x-csrf-token")
        self.user_id = self.get_json_value(response2, "user_id")

    def test_delete_user_by_id_2(self):
        self.login("vinkotov@example.com", "1234")
        # DELETE USER
        response3 = my_req.delete(f"/user/{self.user_id}",
                                  cookies={"auth_sid": self.auth_sid},
                                  headers={"x-csrf-token": self.token}
                                  )
        assert response3.text == 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.', \
            f"Unexpected response text '{response3.text}'"

    def test_delete_user_positive(self):
        self.login()
        # DELETE USER
        response3 = my_req.delete(f"/user/{self.user_id}",
                                  cookies={"auth_sid": self.auth_sid},
                                  headers={"x-csrf-token": self.token}
                                  )
        self.assert_response_status_code(response3, 200)
        # GET USER DETAILS
        response4 = my_req.get(f"/user/{self.user_id}",
                               cookies={"auth_sid": self.auth_sid},
                               headers={"x-csrf-token": self.token}
                               )
        assert response4.text == 'User not found', f"Unexpected response text '{response4.text}'"

    def test_delete_another_user(self):
        # LOGIN FIRST USER
        self.login()
        user_1_id = self.user_id
        username_1 = self.username
        # LOGIN SECOND USER
        self.login()
        # TRY TO DELETE FIRST USER BY AUTH SECOND USER
        response3 = my_req.delete(f"/user/{user_1_id}",
                                  cookies={"auth_sid": self.auth_sid},
                                  headers={"x-csrf-token": self.token}
                                  )
        self.assert_response_status_code(response3, 200)
        # GET USER DETAILS
        response4 = my_req.get(f"/user/{user_1_id}",
                               cookies={"auth_sid": self.auth_sid},
                               headers={"x-csrf-token": self.token}
                               )

        self.assert_response_status_code(response4, 200)
        self.assert_json_value_by_name(response4, "username", username_1,
                                       f"Unexpected result user id {user_1_id} was deleted by user id {self.user_id}")
