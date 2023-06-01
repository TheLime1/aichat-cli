import poe
import os
import subprocess


def chatbot(input_message, bot, dir):
    try:
        # initialize POE client with token
        with open('tokens/poe_token.txt', 'r') as f:  # put your token in token.txt
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


def premuim_chatbot(input_message, bot, current_premium_token, dir):
    premium_tokens_file = os.path.join(dir, "tokens", "premium_tokens.txt")
    token_checked = False  # Flag to track if a valid token has been found

    try:
        if current_premium_token is None:
            # Read premium tokens from file only when no current token is available
            with open(premium_tokens_file, 'r') as f:
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

                token_checked = True  # Set the flag to indicate a valid token has been found
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
                elif "Daily limit reached for" in str(e):
                    print(
                        "Daily limit reached for the chatbot, trying the next token...")
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
            if str(e) in ["Invalid token or no bots are available.", "Invalid or missing token."]:
                print("No valid token available.")
            elif "Daily limit reached for" in str(e):
                print("Daily limit reached for the chatbot.")
            else:
                raise e


def check_poe_token(dir):
    token_file = os.path.join(dir, "tokens", "poe_token.txt")
    if not os.path.isfile(token_file) or os.stat(token_file).st_size == 0:
        return False
    return True


def generate_poe_token(dir):
    gen_file = os.path.join(dir, "token_gen", "token_gen.py")
    print("Token file not found or empty. Generating token...")
    subprocess.run(["python", gen_file], check=True)