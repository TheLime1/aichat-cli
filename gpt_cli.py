import argparse
import poe
import asyncio
import os
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

from gptcli.utils import *
from gptcli.poefunc import *
from gptcli.bardfunc import *
from gptcli.bingfunc import *

dir = os.path.dirname(os.path.abspath(__file__))
conversation = []

SAGE = "capybara"
GPT = "chinchilla"
GPT4 = "beaver"
CLAUDE = "a2"
CLAUDEPLUS = "a2_2"
CLAUDEHUNK = "a2_100k"
BARD = "bard"
BING = "bing"

BOT_COMPLETER = WordCompleter(
    ["sage", "chatgpt", "beaver", "claude", "claudeplus", "claudehunk", "bard", "bing"], ignore_case=True)

BOT_NAME_MAPPING = {
    "sage": SAGE,
    "chatgpt": GPT,
    "beaver": GPT4,
    "claude": CLAUDE,
    "claudeplus": CLAUDEPLUS,
    "claudehunk": CLAUDEHUNK,
    "bard": BARD,
    "bing": BING
}


async def main():
    current_premium_token = None
    if not check_poe_token(dir):
        generate_poe_token(dir)

    parser = argparse.ArgumentParser(
        description='ClI chatbot powered by POE, created by @TheLime1')
    parser.add_argument(
        '-b', '--bot', choices=["sage", "chatgpt", "beaver", "claude", "claudeplus", "claudehunk", "bard", "bing"],
        help='Choose the bot (type sage, chatgpt, beaver, claude, claudeplus, claudehunk, bard or bing)')
    parser.add_argument('-m', '--message',
                        nargs='+', help='Input message for the chatbot')

    args = parser.parse_args()

    if not args.message or not args.bot:
        print(ascii_art)
        bot = change_bot()
        current_bot = BOT_NAME_MAPPING[bot]
    else:
        bot = args.bot
        if bot is None:
            while bot not in BOT_NAME_MAPPING:
                bot = change_bot()
                if bot is None:
                    print("Invalid input, please try again.")
        bot = BOT_NAME_MAPPING[bot]
        current_bot = bot

        input_message = ' '.join(
            args.message) if args.message else "whats your name?"

        if bot == "bing":
            response = await (
                bingbot(input_message, ConversationStyle.balanced))
        elif bot == "bard":
            response = bardbot(input_message, dir)
        else:
            if bot == "beaver" or bot == "claudeplus" or bot == "claudehunk":
                response, current_premium_token = premuim_chatbot(
                    input_message, bot, current_premium_token, dir)
            else:
                response = chatbot(input_message, bot, dir)
        return

    while True:
        print("\n")
        print_menu()
        option = input()
        print("*************")

        if option == "1":
            bot = change_bot()
            current_bot = BOT_NAME_MAPPING[bot]
        elif option == "2":
            insert_clipboard_message(conversation, chatbot, current_bot, dir)
        elif option == "3":
            export_conversation(conversation, ascii_art)
            break
        elif option == "0":
            if current_premium_token is not None:
                close_program(current_premium_token)
            break
        else:
            input_message = option
            if bot == "bing":
                response = await (
                    bingbot(input_message, ConversationStyle.balanced))
            elif bot == "bard":
                response = bardbot(input_message, dir)
            else:
                if bot == "beaver" or bot == "claudeplus" or bot == "claudehunk":
                    response, current_premium_token = premuim_chatbot(
                        input_message, bot, current_premium_token, dir)
                else:
                    response = chatbot(option, current_bot, dir)
            store_conversation(input_message, response,
                               current_bot, conversation)

if __name__ == '__main__':
    asyncio.run(main())
