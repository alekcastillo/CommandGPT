import os 

class OSConfiguration():
    def __init__(self, os_name, terminal_env_var):
        self.os_name = os_name
        self.terminal_env_var = terminal_env_var

    def get_running_terminal(self):
        terminal_path = os.environ.get(self.terminal_env_var)
        if terminal_path:
            return os.path.basename(terminal_path)
            return os.path.basename(os.environ['COMSPEC'])

os_configurations = {
    "nt": OSConfiguration("Windows", "COMSPEC"),
    "posix": OSConfiguration("Linux", "SHELL"),
}

def get_system_information():
    os_code = os.name
    os_configuration = os_configurations.get(os_code)
    if not os_configuration:
        print("This os is not supported")

    os_name = os_configuration.os_name
    running_terminal = os_configuration.get_running_terminal()

    prompt = f"I'm using a {os_name} system and running a {running_terminal} terminal."
    print(prompt)


get_system_information()
