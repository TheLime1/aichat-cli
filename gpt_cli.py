import argparse
import poe
import asyncio
import os
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

from gptcli.utils import *
from gptcli.poefunc import *

dir = os.path.dirname(os.path.abspath(__file__))

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


def print_menu():
    print("-" * 50)
    print("[1] - Change the bot (somtimes buggy)")
    print("[2] - Insert clipboard contents as message")
    print("[3] - Export conversation to .txt file")
    print("[0] - Close the program")
    print("\nType your message or choose an option:\n")


def change_bot():
    global current_bot, bot_input
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


async def main():
    # Check if token.txt is available and not empty
    if not check_poe_token(dir):
        generate_poe_token(dir)

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
    current_bot = bot

    input_message = ' '.join(args.message) if args.message else "hello"

    if bot_input == "3" or bot_input == "5" or bot_input == "6":
        response = premuim_chatbot(
            input_message, bot, current_premium_token, dir)
    else:
        response = chatbot(input_message, bot, dir)

    store_conversation(input_message, response, current_bot, conversation)

    while True:
        print("\n")
        print_menu()
        option = input()
        print("*************")

        if option == "1":
            change_bot()
        elif option == "2":
            insert_clipboard_message(conversation, chatbot, current_bot)
        elif option == "3":
            export_conversation(conversation, ascii_art)
            break
        elif option == "0":
            close_program()
            break
        else:
            input_message = option
            if bot_input == "3" or bot_input == "5" or bot_input == "6":
                # Use the current bot name
                response = premuim_chatbot(
                    input_message, bot, current_premium_token, dir)
            else:
                # Use the current bot name
                response = chatbot(option, current_bot, dir)
            store_conversation(input_message, response,
                               current_bot, conversation)

if __name__ == '__main__':
    asyncio.run(main())
