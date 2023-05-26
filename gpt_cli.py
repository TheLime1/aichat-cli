import argparse
import poe
import asyncio
import os
import subprocess
import pyperclip
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

SAGE = "capybara"
GPT = "chinchilla"
GPT4 = "beaver"
CLAUDE = "a2"
CLAUDEPLUS = "a2_2"
CLAUDEHUNK = "a2_100k"

BOT_COMPLETER = WordCompleter(
    ["sage", "chatgpt", "beaver", "claude", "claudeplus", "claudehunk"], ignore_case=True)

BOT_NAME_MAPPING = {
    "sage": SAGE,
    "chatgpt": GPT,
    "beaver": GPT4,
    "claude": CLAUDE,
    "claudeplus": CLAUDEPLUS,
    "claudehunk": CLAUDEHUNK
}

conversation = []
current_premium_token = None  # Variable to store the current premium token
current_bot = None  # Variable to store the current bot name

ascii_art = '''
    __     _                        ______ __            __ 
   / /    (_)____ ___   ___        / ____// /_   ____ _ / /_
  / /    / // __ `__ \ / _ \      / /    / __ \ / __ `// __/
 / /___ / // / / / / //  __/     / /___ / / / // /_/ // /_  
/_____//_//_/ /_/ /_/ \___/______\____//_/ /_/ \__,_/ \__/  
                          /_____/                           
'''


def chatbot(input_message, bot):
    try:
        # initialize POE client with token
        with open('token.txt', 'r') as f:  # put your token in token.txt
            token = f.read().rstrip()
        client = poe.Client(token)

        # initialize response
        response = ""

        # stream the response from POE client
        for chunk in client.send_message(bot, input_message, with_chat_break=True):
            response += chunk["text_new"]
            print(chunk["text_new"], end="", flush=True)
        return response
    except RuntimeError as e:
        if str(e) == "Invalid token or no bots are available.":
            print("Bad token trying to regenerate.....")
            generate_token()
        else:
            raise e


def premuim_chatbot(input_message, bot):
    try:
        global current_premium_token  # Use the global variable
        if current_premium_token is None:
            # Read premium tokens from file only when no current token is available
            with open('premium_tokens.txt', 'r') as f:
                premium_tokens = f.read().splitlines()
                if len(premium_tokens) > 0:
                    # Store the first token in the list
                    current_premium_token = premium_tokens[0]

        # Try the current premium token
        if current_premium_token:
            try:
                client = poe.Client(current_premium_token)

                # Initialize response
                response = ""

                # Stream the response from POE client
                for chunk in client.send_message(bot, input_message, with_chat_break=True):
                    response += chunk["text_new"]
                    print(chunk["text_new"], end="", flush=True)

                return response

            except RuntimeError as e:
                if str(e) == "Invalid token or no bots are available.":
                    print("Invalid token, trying the next one...")
                    current_premium_token = None  # Reset the current token
                else:
                    raise e

        # If no valid token is found, raise an exception
        raise RuntimeError("No valid token available.")

    except RuntimeError as e:
        if str(e) == "Invalid token or no bots are available.":
            print("No valid token available.")
        else:
            raise e


def print_menu():
    print("-" * 50)
    print("[1] - Change the bot")
    print("[2] - Insert clipboard contents as message")
    print("[3] - Export conversation to .txt file")
    print("[0] - Close the program")
    print("\nType your message or choose an option:\n")


def store_conversation(user_input, bot_response, bot_name):
    conversation.append((user_input, bot_response, bot_name))


def check_token_file():
    if not os.path.isfile("token.txt") or os.stat("token.txt").st_size == 0:
        return False
    return True


def generate_token():
    print("Token file not found or empty. Generating token...")
    subprocess.run(["python", "token_gen.py"], check=True)


async def main():
    # Check if token.txt is available and not empty
    if not check_token_file():
        generate_token()

    parser = argparse.ArgumentParser(
        description='ClI chatbot powered by POE, created by @TheLime1')
    parser.add_argument(
        '-b', '--bot', choices=["sage", "chatgpt", "beaver", "claude", "claudeplus", "claudehunk"],
        help='Choose the bot (type sage, chatgpt, beaver, claude, claudeplus, or claudehunk)')
    parser.add_argument('-m', '--message',
                        nargs='+', help='Input message for the chatbot')

    args = parser.parse_args()

    bot = args.bot
    print(ascii_art)
    if bot is None:
        while bot not in BOT_NAME_MAPPING:
            bot_input = input(
                "[1] - Sage (tweaked 3.5gpt_turbo) 4096 token\n[2] - ChatGPT (default) 4096 token\n[3] - GPT4(slower,more accurate) 8192 token \n[4] - Claude (default, FAST) 4500 token\n[5] - Claude+ (more creative, FASTER) 9000 token\n[6] - Claude_100K (BETA, very long messages) 100000 token\n\nChoose your bot: ")
            if bot_input == "1":
                bot = "sage"
            elif bot_input == "2":
                bot = "chatgpt"
            elif bot_input == "3":
                bot = "beaver"
            elif bot_input == "4":
                bot = "claude"
            elif bot_input == "5":
                bot = "claudeplus"
            elif bot_input == "6":
                bot = "claudehunk"
            else:
                print("Invalid input, please try again.")

    bot = BOT_NAME_MAPPING[bot]
    current_bot = bot  # Store the current bot name

    input_message = ' '.join(args.message) if args.message else "hello"

    if bot_input == "3" or bot_input == "5" or bot_input == "6":
        response = premuim_chatbot(input_message, bot)
    else:
        response = chatbot(input_message, bot)

    while True:
        print("\n")
        store_conversation(input_message, response, current_bot)
        print_menu()
        option = input()
        print("*************")

        if option == "1":
            bot_input = input(
                "[1] - Sage (tweaked 3.5gpt_turbo) 4096 token\n[2] - ChatGPT (default) 4096 token\n[3] - GPT4(slower,more accurate) 8192 token \n[4] - Claude (default, FAST) 4500 token\n[5] - Claude+ (more creative, FASTER) 9000 token\n[6] - Claude_100K (BETA, very long messages) 100000 token\n\nChoose your bot: ")
            if bot_input == "1":
                bot = "sage"
            elif bot_input == "2":
                bot = "chatgpt"
            elif bot_input == "3":
                bot = "beaver"
            elif bot_input == "4":
                bot = "claude"
            elif bot_input == "5":
                bot = "claudeplus"
            elif bot_input == "6":
                bot = "claudehunk"
            else:
                print("Invalid input, please try again.")
            current_bot = bot  # Update the current bot name
        elif option == "2":
            clipboard_text = pyperclip.paste()
            if clipboard_text:
                print("\nClipboard contents:\n")
                print(clipboard_text)
                print("\n")
                option = clipboard_text.strip()
                response = chatbot(option.replace('\n', ' '), current_bot)
                input_message = option
        elif option == "3":
            # Export conversation to .txt file
            filename = input("Enter the file name: ")
            filename += ".txt"
            directory = "conv"  # default name, you can change it
            if not os.path.exists(directory):
                os.makedirs(directory)
            filepath = os.path.join(directory, filename)
            with open(filepath, "w") as file:
                file.write(ascii_art)
                for user_input, bot_response, bot_name in conversation:
                    file.write("#######################\n")
                    file.write(f"**USER**: {user_input}\n")
                    file.write(f"**BOT ({bot_name})**: {bot_response}\n")
                file.write("\n***conversation exported by limebot_cli***")
                file.close()
            print(f"Conversation exported to {filepath}.")
            break
        elif option == "0":
            break
        else:
            input_message = option
            if bot_input == "3" or bot_input == "5" or bot_input == "6":
                # Use the current bot name
                response = premuim_chatbot(input_message, current_bot)
            else:
                # Use the current bot name
                response = chatbot(option, current_bot)


if __name__ == '__main__':
    asyncio.run(main())
