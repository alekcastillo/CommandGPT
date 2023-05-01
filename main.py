import sys, os, subprocess, json, requests

API_KEY = "REPLACE_WITH_YOUR_OPEN_AI_KEY"
API_URL = "https://api.openai.com/v1/chat/completions"

def _get_kernel_information():
    return subprocess.check_output(['uname', '-a'])

def _find_command_with_gpt(kernel_info: str, command_description: str):
    system_initial_message = f"""
    Act like a Linux expert.
    Consider the following Kernel information: {kernel_info}
    I describe what I want to do on my system.
    You will respond just with the command to do it.
    Nothing more than the command.
    """
    messages = [
        {"role": "system", "content": system_initial_message},
        {"role": "user", "content": command_description}
    ]
    data = {
        "model": "gpt-3.5-turbo",
        "messages": messages,
        "max_tokens": 3062,
        "n": 1,
        "stop": None,
        "temperature": 0.5,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }
    response = requests.post(API_URL, headers=headers, data=json.dumps(data))
    response_json = response.json()
    return response_json

def _run_command(command):
    os.system(command)

def main(args):
    kernel_information = _get_kernel_information()
    command_description = ' '.join(args)
    summary = _find_command_with_gpt(kernel_information, command_description)
    command = summary.get("choices")[0].get("message").get("content")
    _run_command(command)

if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)