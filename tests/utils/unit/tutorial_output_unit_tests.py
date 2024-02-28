import filecmp
import shutil

import pytest

from docs.utils.script_tutorial_output_automation import *


def test_change_json():
    json_md_test = '```json\n {\n "a": "b",\n "b": "c"\n }\n ```'
    assert change_json_to_tempvalue(json_md_test,0) == "changeThis"
    json_md_not_good = '```json\n {\n "a": "b",\n "b": "c"\n }\n'
    assert change_json_to_tempvalue(json_md_not_good,0) != "changeThis"


def test_find_curl_commands():
    curl_to_find = "```bash\ncurl https://www.google.com\n``` \n ```bash\ncurl -I https://www.google.com\n```"
    found_curl_commands = [x[0] for x in find_curl_commands(curl_to_find)]
    assert found_curl_commands == ['curl https://www.google.com', 'curl -I https://www.google.com']
    incorrect_bash_command = "```bash\n ping https://www.google.com\n``` \n ```bash\ncurl -I https://www.google.com\n```"
    found_curl_commands = [x[0] for x in find_curl_commands(incorrect_bash_command)]
    assert found_curl_commands == ['curl -I https://www.google.com']


def test_execute_curl():
    curl_to_test = """curl -X 'POST' \
  'http://localhost:5000/v1/consumption_profile/cpu' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
   "cpu": {
    "name": "intel xeon gold 6134",
    "tdp": 130
    }
  }'
"""
    assert execute_curl(curl_to_test) == '{"a":35.5688,"b":0.2438,"c":9.6694,"d":-0.6087}' # Change to verify if valid json is returned


def test_replace_curl_command():
    curl_commands = ["""curl -X 'POST' 
  '{{ endpoint }}/v1/component/cpu?verbose=false&allocation=TOTAL' 
  -H 'accept: application/json' 
  -H 'Content-Type: application/json' 
  -d '{
  "name": "intel xeon gold 6134"
}'"""]
    curl_commands = replace_curl_with_localhost(curl_commands)

    assert "localhost:5000" in curl_commands[0]


def test_parse_result_to_json():
    result = '{"a":35.5688,"b":0.2438,"c":9.6694,"d":-0.6087}'
    assert parse_result_to_json(result) == """```json
{
    "a": 35.5688,
    "b": 0.2438,
    "c": 9.6694,
    "d": -0.6087
}
```"""


def test_replace_placeholder_by_json():
    json_exemple = '{\n    "a": 35.5688,\n    "b": 0.2438,\n    "c": 9.6694,\n    "d": -0.6087\n}'
    placeholder_to_change = "changeThis"
    assert replace_placeholder_by_json(json_exemple, placeholder_to_change) == json_exemple

