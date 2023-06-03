# this file is compatible with github actions

import poe
import os


def remove_bad_tokens():
    # Get the current working directory, which is the repository root in GitHub Actions
    repo_root = os.getcwd()

    premium_tokens_file = os.path.join(
        repo_root, "tokens", "premium_tokens.txt")
    valid_tokens = []
    unchecked_tokens = []
    bad_tokens = []
    consecutive_valid_tokens = 0

    try:
        with open(premium_tokens_file, 'r') as f:
            premium_tokens = f.read().splitlines()

        # Move all tokens to the unchecked_tokens list initially
        unchecked_tokens.extend(premium_tokens)

        for token in unchecked_tokens:
            try:
                client = poe.Client(token)
                valid_tokens.append(token)
                consecutive_valid_tokens += 1

                if consecutive_valid_tokens == 3:
                    break  # Stop the program when there are three consecutive valid tokens

            except RuntimeError:
                bad_tokens.append(token)
                print(f"Removing bad token: {token}")
                consecutive_valid_tokens = 0

        with open(premium_tokens_file, 'w') as f:
            f.write('\n'.join(valid_tokens))
            f.write('\n'.join(unchecked_tokens[len(valid_tokens):]))

    except FileNotFoundError:
        print("premium_tokens.txt file not found.")

    print("Valid tokens:")
    print(valid_tokens)

    print("Remaining unchecked tokens:")
    print(unchecked_tokens[len(valid_tokens):])

    print("Bad tokens:")
    print(bad_tokens)


# Usage example
remove_bad_tokens()
