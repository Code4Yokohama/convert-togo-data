import json
from jsonschema import validate, ValidationError


with open('schema.json') as file_obj:
    json_schema = json.load(file_obj)

json_open = open('sample.json', 'r')
json_input = json.load(json_open)

try:
    validate(json_input, json_schema)
except ValidationError as e:
    print(e.message)

print('End')

