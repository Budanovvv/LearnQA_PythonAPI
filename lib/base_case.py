from datetime import datetime
import json
from requests import Response


class BaseCase:

    def get_cookie(self, response: Response, cookies_name):
        assert cookies_name in response.cookies, f"Can't find cookie with the name {cookies_name} in response"
        return response.cookies[cookies_name]

    def get_header(self, response: Response, headers_name):
        assert headers_name in response.headers, f"Can't find header with the name {headers_name} in response"
        return response.headers[headers_name]

    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response not in JSON format. Response text is '{response.text}'"
        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"
        return response_as_dict[name]

    def prepare_registration_data(self, email=None):
        if email is None:
            rnd_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{rnd_part}_@example.com"
        return {
            "password": "123",
            "username": "learnqa",
            "firstName": "learnqa",
            "lastName": "learnqa",
            "email": email
        }


