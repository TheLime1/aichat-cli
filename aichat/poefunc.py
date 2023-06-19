import poe
import os
import subprocess
import requests
import requests
from io import StringIO

def chatbot(input_message, bot, dir):
    try:
        # initialize POE client with token
        with open('tokens/poe_token.txt', 'r') as f:
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
        if str(e) in ["Invalid token or no bots are available.", "Invalid or missing token."]:
            print("Bad token, trying to regenerate...")
            generate_poe_token(dir)
        else:
            raise e


def get_premium_tokens_from_link(link):
    response = requests.get(link)
    if response.status_code == 200:
        token_data = response.text
        token_file = StringIO(token_data)
        premium_tokens = token_file.read().splitlines()
        return premium_tokens
    else:
        raise RuntimeError("Failed to retrieve premium tokens from the link.")

def premuim_chatbot(input_message, bot, current_premium_token, dir):
    premium_tokens_link = "https://raw.githubusercontent.com/TheLime1/online-proxy-list/main/poe_token_check/poe_tokens.txt"
    token_checked = False  # Flag to track if a valid token has been found

    try:
        if current_premium_token is None:
            # Retrieve premium tokens from the link only when no current token is available
            premium_tokens = get_premium_tokens_from_link(premium_tokens_link)
            if len(premium_tokens) > 0:
                # Store the first token in the list
                current_premium_token = premium_tokens[0]

        # Try the current premium token or the next available token
        while current_premium_token:
            try:
                client = poe.Client(current_premium_token)

                # Initialize response
                response = ""

                # Stream the response from POE client
                for chunk in client.send_message(bot, input_message, with_chat_break=True):
                    response += chunk["text_new"]
                    print(chunk["text_new"], end="", flush=True)

                token_checked = True  # Set the flag to indicate a valid token has been found
                return response, current_premium_token

            except RuntimeError as e:
                error_messages = ["Invalid token or no bots are available.", "Invalid or missing token.",
                                  "Daily limit reached for", "Daily limit reached for capybara.",
                                  "Invalid token or no bots are available.",
                                  "Invalid or missing token.",
                                  "Daily limit reached for chinchilla.",
                                  "Daily limit reached for beaver.",
                                  "Daily limit reached for a2.",
                                  "Daily limit reached for a2_2.",
                                  "Daily limit reached for a2_100k."]
                if any(error_message in str(e) for error_message in error_messages):
                    if "Daily limit reached for" in str(e):
                        print("Daily limit reached for the chatbot, trying the next token...")
                    else:
                        print("Invalid token, trying the next one...")

                    # Remove the current token from the list
                    premium_tokens = premium_tokens[1:]
                    if len(premium_tokens) > 0:
                        # Store the next token in the list
                        current_premium_token = premium_tokens[0]
                    else:
                        # No more tokens to try, raise an exception
                        raise RuntimeError("No valid token available.")
                else:
                    raise e

        # If no valid token is found, raise an exception
        raise RuntimeError("No valid token available.")

    except RuntimeError as e:
        if not token_checked:
            if any(error_message in str(e) for error_message in error_messages):
                if "Daily limit reached for" in str(e):
                    print("Daily limit reached for the chatbot.")
                else:
                    print("No valid token available.")
            else:
                raise e


def check_poe_token(dir):
    token_file = os.path.join(dir, "tokens", "poe_token.txt")
    if not os.path.isfile(token_file) or os.stat(token_file).st_size == 0:
        return False
    return True


def generate_poe_token(dir):
    # TODO: change to poe_token_gen.py
    gen_file = os.path.join(dir, "token_gen", "token_gen.py")
    print("Token file not found or empty. Generating token...")
    subprocess.run(["python", gen_file], check=True)


def delete_chat(current_premium_token):
    shared_bots = ["beaver", "a2_2", "a2_100k"]
    client = poe.Client(current_premium_token)
    for bot in shared_bots:
        client.purge_conversation(bot)
        print("Chat history deleted for " + bot)
