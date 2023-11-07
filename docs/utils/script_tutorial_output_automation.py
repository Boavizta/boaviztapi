import json
import os
import re
import subprocess
import typing


def change_json_to_tempvalue(read_file: str):
    regex_to_find_json_in_md = r"```json\w*[^`]+```*"
    return re.sub(regex_to_find_json_in_md, "changeThis", read_file)


def find_curl_commands(read_file: str):
    regex_to_find_curl_in_md = r"```bash\s*([\s\S]*?)```"
    return re.findall(regex_to_find_curl_in_md, read_file)


def replace_curl_with_localhost(read_curl: typing.List[str]):
    for i in range(0, len(read_curl)):
        read_curl[i] = read_curl[i].replace("https://api.boavizta.org", "http://localhost:5000")
    return read_curl


def execute_curl(curl_to_execute: str):
    curl_to_execute = re.sub(r'^```bash\n|\n```|#.*\n', '', curl_to_execute)
    curl_to_execute = "curl --no-progress-meter" + curl_to_execute[4::]
    return subprocess.check_output(curl_to_execute, shell=True).decode("utf-8")


def parse_result_to_json(result: str):
    result = json.loads(result)
    result = json.dumps(result, sort_keys=False, indent=4, separators=(",", ":"))
    result = "```json\n" + result + "\n```"
    return result


def replace_placeholder_by_json(curl_results: str, file_to_replace: str):
    return file_to_replace.replace("changeThis", curl_results, 1)


def add_all_json_results_to_md(found_curl_commands: typing.List[str], read_file_to_replace: str):
    for i in range(0, len(found_curl_commands)):
        curl_result = execute_curl(found_curl_commands[i])
        curl_result = parse_result_to_json(curl_result)
        read_file_to_replace = replace_placeholder_by_json(curl_result, read_file_to_replace)
    return read_file_to_replace


def change_one_read_file(file_content: str):
    found_curl_commands = find_curl_commands(file_content)
    found_curl_commands = replace_curl_with_localhost(found_curl_commands)
    file_with_json_placeholder = change_json_to_tempvalue(file_content)
    return add_all_json_results_to_md(found_curl_commands, file_with_json_placeholder)


def generate_tutorial_output(directory_to_check: str):
    list_of_files = [file for file in os.listdir(directory_to_check) if file.endswith(".md")]
    for file_name in list_of_files:
        with(open(directory_to_check + "/" + file_name, "r+") as file):
            changed_file = change_one_read_file(file.read())
            file.seek(0)
            file.write(changed_file)
            file.truncate()


if __name__ == "__main__":
    generate_tutorial_output("../docs/getting_started")
