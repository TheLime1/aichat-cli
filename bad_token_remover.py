# this file is compatible with github actions

import poe
import os


def remove_bad_tokens():
    repo_root = os.getcwd()

    premium_tokens_file = os.path.join(
        repo_root, "aichat", "tokens", "premium_tokens.txt")
    valid_tokens = []
    unchecked_tokens = []
    bad_tokens = []
    consecutive_valid_tokens = 0

    try:
        with open(premium_tokens_file, 'r') as f:
            premium_tokens = f.read().splitlines()

        # Move all tokens to the unchecked_tokens list initially
        unchecked_tokens.extend(premium_tokens)

        for token in premium_tokens:
            try:
                client = poe.Client(token)
                valid_tokens.append(token)
                consecutive_valid_tokens += 1
                print(f"Valid token: {token}")

                if consecutive_valid_tokens == 1000:
                    break  # Stop the program when there are three consecutive valid tokens

            except RuntimeError:
                bad_tokens.append(token)
                print(f"Removing bad token: {token}")
                consecutive_valid_tokens = 0
            finally:
                # Remove the checked token from the unchecked_tokens list
                unchecked_tokens.remove(token)

        if consecutive_valid_tokens < 3:
            # Add the remaining unchecked tokens to the valid_tokens list
            valid_tokens.extend(unchecked_tokens)

        with open(premium_tokens_file, 'w') as f:
            # Write the valid_tokens first, followed by the remaining unchecked_tokens
            f.write('\n'.join(valid_tokens + unchecked_tokens))

    except FileNotFoundError:
        print("premium_tokens.txt file not found.")

    print("Valid tokens:")
    print(valid_tokens)

    print("Unchecked tokens:")
    print(unchecked_tokens)

    print("Bad tokens:")
    print(bad_tokens)


# Usage example
remove_bad_tokens()
