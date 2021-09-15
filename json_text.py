import json

json_text = '{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},{"message":"And ' \
            'this is a second message","timestamp":"2021-06-04 16:41:01"}]} '

parsed_json = json.loads(json_text)

print(parsed_json["messages"][0]["message"])
