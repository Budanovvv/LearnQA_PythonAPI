import json

import requests
import pytest


class TestUserAgent:
    with open("user_agent.json") as jsonFile:
        jsonObject = json.load(jsonFile)
        jsonFile.close()

    @pytest.mark.parametrize('test_data', jsonObject)
    def test_user_agent(self, test_data):
        response = requests.get('https://playground.learnqa.ru/ajax/api/user_agent_check',
                                headers={"User-Agent": test_data["header"]})

        response_dict = response.json()
        print(response_dict)
        assert "user_agent" in response_dict, 'There is no key "user_agent" in response'
        assert "platform" in response_dict, 'There is no key "platform" in response'
        assert "browser" in response_dict, 'There is no key "browser" in response'
        assert "device" in response_dict, 'There is no key "device" in response'
        act_platform = response_dict["platform"]
        act_browser = response_dict["browser"]
        act_device = response_dict["device"]
        assert act_platform == test_data["platform"], \
            f'platform {act_platform} is wrong,expected data: platform - {test_data["platform"]},' \
            f' browser - {test_data["browser"]}, device - {test_data["device"]}'
        assert act_browser == test_data["browser"], \
            f'browser {act_browser} is wrong,expected data:  platform {test_data["platform"]},' \
            f' browser {test_data["browser"]}, device {test_data["device"]}'
        assert act_device == test_data["device"], \
            f'device {act_device} is wrong,expected data:  platform - {test_data["platform"]},' \
            f' browser - {test_data["browser"]}, device - {test_data["device"]}'
