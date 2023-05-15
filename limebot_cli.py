import argparse
import poe
import asyncio
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

SAGE = "capybara"
GPT = "chinchilla"
BOT_COMPLETER = WordCompleter([SAGE, GPT], ignore_case=True)


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
    bot = ""
    while bot not in [SAGE, GPT]:
        bot_input = input("Enter 1 for Sage, 2 for GPT: ")
        if bot_input == "1":
            bot = SAGE
        elif bot_input == "2":
            bot = GPT
        else:
            print("Invalid input, please try again.")

    input_message = input("Input message for the chatbot: ")

    response = chatbot(input_message, bot)

    print(response)


if __name__ == '__main__':
    asyncio.run(main())
