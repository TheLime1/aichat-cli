from bardapi import Bard
import os


def bardbot(input_message, dir):
    if not check_bard_token(dir):
        print("Check README for instructions on how to generate Bard token manually.")
        raise RuntimeError("No valid Bard token available.")
    else:
        with open('tokens/bard_token.txt', 'r') as f:
            token = f.read().rstrip()
        bard = Bard(token)
        response = (bard.get_answer(input_message)['content'])
        print(response)
        return response


def check_bard_token(dir):
    token_file = os.path.join(dir, "tokens", "bard_token.txt")
    if not os.path.isfile(token_file) or os.stat(token_file).st_size == 0:
        return False
    return True
