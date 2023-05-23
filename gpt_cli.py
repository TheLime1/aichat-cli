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
BOT_COMPLETER = WordCompleter(["sage", "chatgpt"], ignore_case=True)

BOT_NAME_MAPPING = {
    "sage": SAGE,
    "chatgpt": GPT
}

conversation = []

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


def print_menu():
    print("-" * 50)
    print("[1] - Change the bot")
    print("[2] - Insert clipboard contents as message")
    print("[3] - Export conversation to .txt file")
    print("[0] - Close the program")
    print("\nType your message or choose an option:\n")


def store_conversation(user_input, bot_response):
    conversation.append((user_input, bot_response))


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
        '-b', '--bot', choices=["sage", "chatgpt"], help='Choose the bot (type sage or chatgpt)')
    parser.add_argument('-m', '--message',
                        nargs='+', help='Input message for the chatbot')

    args = parser.parse_args()

    bot = args.bot
    print(ascii_art)
    if bot is None:
        while bot not in BOT_NAME_MAPPING:
            bot_input = input("[1] - Sage\n[2] - ChatGPT\n\nChoose your bot: ")
            if bot_input == "1":
                bot = "sage"
            elif bot_input == "2":
                bot = "chatgpt"
            else:
                print("Invalid input, please try again.")

    bot = BOT_NAME_MAPPING[bot]

    input_message = ' '.join(args.message) if args.message else "hello"

    response = chatbot(input_message, bot)

    while True:
        print("\n")
        store_conversation(input_message, response)
        print_menu()
        option = input()
        print("*************")

        if option == "1":
            bot_input = input("[1] - Sage\n[2] - ChatGPT\n\nChoose your bot: ")
            if bot_input == "1":
                bot = "sage"
            elif bot_input == "2":
                bot = "chatgpt"
            else:
                print("Invalid input, please try again.")
        elif option == "2":
            clipboard_text = pyperclip.paste()
            if clipboard_text:
                print("\nClipboard contents:\n")
                print(clipboard_text)
                print("\n")
                option = clipboard_text.strip()
                response = chatbot(option.replace('\n', ' '), bot)
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
                for user_input, bot_response in conversation:
                    file.write("#######################\n")
                    file.write(f"**USER**: {user_input}\n")
                    file.write(f"**BOT**: {bot_response}\n")
                file.write("\n***conversation exported by limebot_cli***")
                file.close()
            print(f"Conversation exported to {filepath}.")
            break
        elif option == "0":
            break
        else:
            response = chatbot(option, bot)
            input_message = option


if __name__ == '__main__':
    asyncio.run(main())
