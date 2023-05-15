import argparse
import poe
import asyncio
import os
import subprocess
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

SAGE = "capybara"
GPT = "chinchilla"
BOT_COMPLETER = WordCompleter(["sage", "chatgpt"], ignore_case=True)

BOT_NAME_MAPPING = {
    "sage": SAGE,
    "chatgpt": GPT
}


def chatbot(input_message, bot):
    # initialize POE client with token
    with open('token.txt', 'r') as f:  # put your token in token.txt
        token = f.read().rstrip()
    client = poe.Client(token)

    # initialize response
    response = ""

    # stream the response from POE client
    for chunk in client.send_message(bot, input_message, with_chat_break=True):
        response += chunk["text_new"]
    return response


async def main():
    # Check if token.txt is available and not empty
    if not os.path.isfile("token.txt") or os.stat("token.txt").st_size == 0:
        print("Token file not found or empty. Generating token...")
        subprocess.run(["python", "token_gen.py"], check=True)

    parser = argparse.ArgumentParser(
        description='ClI chatbot powered by POE, created by @TheLime1')
    parser.add_argument(
        '-b', '--bot', choices=["sage", "chatgpt"], help='Choose the bot (type sage or chatgpt)')
    parser.add_argument('-m', '--message',
                        help='Input message for the chatbot')

    args = parser.parse_args()

    bot = args.bot
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

    input_message = args.message
    if input_message is None:
        input_message = input("Input message for the chatbot: ")

    response = chatbot(input_message, bot)

    print(response)


if __name__ == '__main__':
    asyncio.run(main())
