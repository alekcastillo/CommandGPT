import sys, os, json, requests, psutil

API_KEY = "REPLACE_WITH_YOUR_OPEN_AI_KEY"
API_URL = "https://api.openai.com/v1/chat/completions"

OS_NAMES = {
    "nt": "Windows",
    "posix": "Linux",
}

def _get_os_name():
    os_code = os.name
    os_name = OS_NAMES.get(os_code)
    if not os_name:
        raise Exception("This os is not supported")

    return os_name

def _get_running_terminal_name():
    parent_pid = os.getppid()
    return psutil.Process(parent_pid).name().replace('.exe', '')

def _find_command_with_gpt(os_name: str, running_terminal: str, command_description: str, first_command: str=None):
    system_initial_message = f"""
    Act like an OS CLI expert.
    I'm using the {running_terminal} terminal on a {os_name} system.
    I will describe what I want to do on my system.
    You will respond just with the command to do it.
    No text before or after the command.
    """
    messages = [
        {"role": "system", "content": system_initial_message},
        {"role": "user", "content": command_description}
    ]
    if first_command:
        messages.append({"role": "user", "content": f"Other than {first_command}"})

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

def _get_terminal_command_flag(os_name: str, terminal: str):
    if os_name == "Linux":
        return "-c"

    if terminal == "cmd":
        return "/C"

    return ""

def _run_command(terminal: str, command_flag: str, command: str):
    return os.system(f'{terminal} {command_flag} "{command}"')

def main(args):
    command_description = ' '.join(args)
    os_name = _get_os_name()
    running_terminal = _get_running_terminal_name()
    print(f"Using the {running_terminal} terminal on a {os_name} system...")

    generating = True
    command = None

    while (generating):
        summary = _find_command_with_gpt(os_name, running_terminal, command_description, command)
        command = summary.get("choices")[0].get("message").get("content").strip().replace('`', '')

        print(f"Found the following command: {command}")

        user_input = input("Do you wish to run it (y/n/r - Regenerate)? ")
        if user_input == 'r':
            continue
        elif user_input != 'y':
            return
        
        generating = False

    command_flag = _get_terminal_command_flag(os_name, running_terminal)
    _run_command(running_terminal, command_flag, command)

if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)
