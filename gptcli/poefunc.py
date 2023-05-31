import poe
import os
import subprocess


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
        if str(e) in ["Invalid token or no bots are available.", "Invalid or missing token."]:
            print("Bad token, trying to regenerate...")
            generate_poe_token()
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

                return response

            except RuntimeError as e:
                if str(e) in ["Invalid token or no bots are available.", "Invalid or missing token."]:
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
        if str(e) in ["Invalid token or no bots are available.", "Invalid or missing token."]:
            print("No valid token available.")
        else:
            raise e


def check_poe_token():
    if not os.path.isfile("token.txt") or os.stat("token.txt").st_size == 0:
        return False
    return True


def generate_poe_token():
    print("Token file not found or empty. Generating token...")
    subprocess.run(["python", "token_gen.py"], check=True)
