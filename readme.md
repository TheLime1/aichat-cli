# GPT CLI v0.1

A command-line interface chatbot. It allows you to have interactive conversations with different bots, including GPT4 FOR FREE

Check the web version [here](https://github.com/TheLime1/gptCensorFree).

Thanks to [@Lomusire](https://github.com/Lomusire) for providing premium tokens ❤️.

## Features

- Choose between different bots.
- Input messages for the chatbot via command-line arguments or interactively.
- Export the conversation to a .txt file for future reference.

## Prerequisites

- Python 3.7 or higher installed on your system.

## Getting Started

1. Clone or download the GPT CLI repository to your local machine.

2. Open a command-line interface (e.g., Command Prompt, Terminal) and navigate to the directory where you have saved the GPT CLI files.

3. Install the required dependencies by running the following command:
```
pip install -r requirements.txt
```

4. Run the GPT CLI app:
```
python gpt_cli.py
```

## Usage

The GPT CLI supports the following command-line arguments:

- `-b` or `--bot`: Choose the bot for the conversation. Valid options are provided by the application.
Example: `python gpt_cli.py -b chatgpt`

- `-m` or `--message`: Input a message for the chatbot.
Example: `python gpt_cli.py -b sage -m "Hello, how are you?"`

- For more info, use `-h` or `--help` to see the help message.

If you don't provide any command-line arguments, the app will prompt you to choose a bot and enter a message interactively.

Once the conversation starts, you can continue the interaction by typing your messages or selecting options from the menu. The menu options include changing the bot or exporting the conversation to a .txt file.

## Notes

- If the app cannot find the `token.txt` file or the file is empty, it will automatically generate a new token using the `token_gen.py` script provided.

- The GPT CLI app also supports the use of premium tokens , so you can be able to use GPT4.

- The conversation history is stored within the app and is not persistent between sessions.

Feel free to customize and enhance the GPT CLI app according to your needs. Happy **chatting**!

![WindowsTerminal_ayTEloGZs7](https://github.com/TheLime1/gpt-cli/assets/47940043/e695eebc-84fb-46d1-bb05-281511994799)

