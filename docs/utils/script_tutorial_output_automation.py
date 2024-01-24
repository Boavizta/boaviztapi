import json
import os
import re
import subprocess
import typing
from uvicorn import Config
from boaviztapi.main import app, UvicornServerThreaded

"""
script_tutorial_output_automation.py

Description : This file contains all the functions needed for automate the "getting started" part of the documentation.
The code iterates over all doc files of this part, and search for every curl command in bash code bloc on the markdown,
execute them and replace the nearest json after the curl command by the result of the command.
"""


def change_json_to_tempvalue(read_file: str, index_to_change):
    regex_to_find_json_in_md = r"```json\w*[^`]+```*"
    json_to_change = read_file[index_to_change:]
    file_until_json = read_file[:index_to_change]
    json_to_change = re.sub(regex_to_find_json_in_md, "changeThis", json_to_change, count=1)
    return f"{file_until_json}{json_to_change}"


def find_curl_commands(read_file: str):
    regex_to_find_curl_in_md = r"```bash\s*([\s\S]*?)```"
    result = re.finditer(regex_to_find_curl_in_md, read_file)
    curl_command = []
    for bash_command in result:
        bash_found = bash_command.group()
        if "curl" in bash_found:
            bash_found = re.sub(r'^```bash\n|\n```|#.*\n', '', bash_found)
            curl_command.append([bash_found, bash_command.end()])
    return curl_command


def replace_curl_with_localhost(read_curl: typing.List[str]):
    for i in range(0, len(read_curl)):
        read_curl[i] = read_curl[i].replace("{{ endpoint }}", "http://localhost:5000")
    return read_curl


def execute_curl(curl_to_execute: str):
    curl_to_execute = f"curl --no-progress-meter {curl_to_execute[4::]}"
    return subprocess.check_output(curl_to_execute, shell=True).decode("utf-8")


def parse_result_to_json(result: str):
    result = json.loads(result)
    result = json.dumps(result, sort_keys=False, indent=4)
    result = f"```json\n{result}\n```"
    return result


def replace_placeholder_by_json(curl_results: str, file_to_replace: str):
    return file_to_replace.replace("changeThis", curl_results, 1)


def add_all_json_results_to_md(found_curl_commands: typing.List[str], read_file_to_replace: str, index_of_curl_commands:
typing.List[str]):
    for i in range(0, len(found_curl_commands)):
        read_file_to_replace = change_json_to_tempvalue(read_file_to_replace, int(index_of_curl_commands[i]))
        curl_result = execute_curl(found_curl_commands[i])
        curl_result = parse_result_to_json(curl_result)
        read_file_to_replace = replace_placeholder_by_json(curl_result, read_file_to_replace)
    return read_file_to_replace


def change_one_read_file(file_content: str):
    found_curl_commands = find_curl_commands(file_content)
    list_of_curl_commands = [curl_commands[0] for curl_commands in found_curl_commands]
    index_curl_commands = [index[1] for index in found_curl_commands]
    found_curl_commands = replace_curl_with_localhost(list_of_curl_commands)
    return add_all_json_results_to_md(found_curl_commands, file_content, index_curl_commands)


def generate_tutorial_output(directory_to_check: str):
    list_of_files = [file for file in os.listdir(directory_to_check) if file.endswith(".md")]
    for file_name in list_of_files:
        with(open(f"{directory_to_check}/{file_name}", "r+") as file):
            changed_file = change_one_read_file(file.read())
            file.seek(0)
            file.write(changed_file)
            file.truncate()


if __name__ == "__main__":
    config = Config(app=app, host='localhost', port=5000, reload=True)
    server = UvicornServerThreaded(config=config)
    with server.run_in_thread():
        # run the script
        generate_tutorial_output("../docs/getting_started")
