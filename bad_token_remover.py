import poe
import os


def remove_bad_tokens(dir):
    premium_tokens_file = os.path.join(dir, "tokens", "premium_tokens.txt")
    unchecked_tokens = []
    valid_tokens = []
    bad_tokens = []
    consecutive_valid_tokens = 0

    try:
        with open(premium_tokens_file, 'r') as f:
            premium_tokens = f.read().splitlines()
            unchecked_tokens = premium_tokens.copy()

        for token in premium_tokens:
            try:
                client = poe.Client(token)
                valid_tokens.append(token)
                consecutive_valid_tokens += 1
                unchecked_tokens.remove(token)
                print(f"Valid token: {token}")

                if consecutive_valid_tokens == 3:
                    break

            except RuntimeError:
                bad_tokens.append(token)
                unchecked_tokens.remove(token)
                print(f"Removing bad token: {token}")
                consecutive_valid_tokens == 0

        with open(premium_tokens_file, 'w') as f:
            f.write('\n'.join(valid_tokens + unchecked_tokens))

    except FileNotFoundError:
        print("premium_tokens.txt file not found.")


# Usage example
dir = os.path.dirname(os.path.abspath(__file__))
remove_bad_tokens(dir)
