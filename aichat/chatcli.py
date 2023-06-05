import argparse
import asyncio
import os
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

from utils import *
from poefunc import *
from bardfunc import *
from bingfunc import *

dir = os.path.dirname(os.path.abspath(__file__))
conversation = []

BOTS = {
    "sage": "capybara",
    "chatgpt": "chinchilla",
    "gpt4": "beaver",
    "claude": "a2",
    "claudeplus": "a2_2",
    "claudehunk": "a2_100k",
    "bard": "bard",
    "bing": "bing"
}

BOT_COMPLETER = WordCompleter(list(BOTS.keys()), ignore_case=True)


async def main():
    current_premium_token = None
    if not check_poe_token(dir):
        generate_poe_token(dir)

    parser = argparse.ArgumentParser(
        description='ClI chatbot powered by POE, created by @TheLime1')
    parser.add_argument('-b', '--bot', choices=list(BOTS.keys()),
                        help='Choose the bot (type sage, chatgpt, gpt4, claude, claudeplus, claudehunk, bard or bing)')
    parser.add_argument('-m', '--message', nargs='+',
                        help='Input message for the chatbot')

    args = parser.parse_args()

    if not args.message or not args.bot:
        print(ascii_art)
        bot = change_bot()
        current_bot = BOTS[bot]
    else:
        bot = args.bot
        current_bot = BOTS.get(bot)
        if not current_bot:
            print("Invalid input, please try again.")
            return

        input_message = ' '.join(
            args.message) if args.message else "whats your name?"

        if current_bot == "bing":
            response = await bingbot(input_message, ConversationStyle.balanced)
        elif current_bot == "bard":
            response = bardbot(input_message, dir)
        elif current_bot in ["beaver", "a2_2", "a2_100k"]:
            response, current_premium_token = premuim_chatbot(
                input_message, current_bot, current_premium_token, dir)
        else:
            response = chatbot(input_message, current_bot, dir)
        return

    while True:
        print("\n")
        print_menu()
        option = input()
        print("*************")

        if option == "1":
            bot = change_bot()
            current_bot = BOTS[bot]
        elif option == "2":
            clip_board = insert_clipboard_message()
            input_message = clip_board
            if current_bot == "bing":
                response = await bingbot(input_message, ConversationStyle.balanced)
            elif current_bot == "bard":
                response = bardbot(input_message, dir)
            elif current_bot in ["beaver", "a2_2", "a2_100k"]:
                response, current_premium_token = premuim_chatbot(
                    input_message, current_bot, current_premium_token, dir)
            else:
                response = chatbot(input_message, current_bot, dir)
            store_conversation(input_message, response,
                               current_bot, conversation)
        elif option == "3":
            export_conversation(conversation, ascii_art)
            break
        elif option == "0":
            if current_premium_token is not None:
                close_program(current_premium_token)
            break
        else:
            input_message = option
            if current_bot == "bing":
                response = await bingbot(input_message, ConversationStyle.balanced)
            elif current_bot == "bard":
                response = bardbot(input_message, dir)
            elif current_bot in ["beaver", "a2_2", "a2_100k"]:
                response, current_premium_token = premuim_chatbot(
                    input_message, current_bot, current_premium_token, dir)
            else:
                response = chatbot(input_message, current_bot, dir)
            store_conversation(input_message, response,
                               current_bot, conversation)


if __name__ == '__main__':
    asyncio.run(main())
