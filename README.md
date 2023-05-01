# CommandGPT

Just a small POC of a Python-based CLI tool capable of turning human descriptions into Linux commands using GPT.
This is currently in very bad shape, but I'll continue improving it for those interested :).

## Setup

You can use the included setup script, which creates a VirtualEnv and installs the required dependencies:

    ./setup_env.sh

Then replace the `API_KEY` variable in the *main.py* file with your [OpenAI API Key](https://platform.openai.com/account/api-keys).

## Usage

Just run the script followed by the description of the command you wish to run.
**Example:**

    ./python main.py Show me my current user
