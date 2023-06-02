import poe
import requests
import os


def create_pull_request(repo_owner, repo_name, branch, title, body, file_path, file_content):
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls"
    headers = {
        "Authorization": f"Bearer {os.environ.get['G_TOKEN']}",
        "Accept": "application/vnd.github.v3+json"
    }

    payload = {
        "title": title,
        "body": body,
        "head": branch,
        "base": "main",
        "maintainer_can_modify": True,
        "draft": False,
    }

    # Create the pull request
    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code == 201:
        pull_request = response.json()
        pr_number = pull_request["number"]
        pr_url = pull_request["html_url"]
        print(f"Pull request created: {pr_url}")

        # Create a commit with the modified file in the pull request
        commit_message = f"Update {file_path}"
        commit_payload = {
            "message": commit_message,
            "content": file_content,
            "branch": branch
        }

        commit_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
        response = requests.put(
            commit_url, headers=headers, json=commit_payload)

        if response.status_code == 201:
            print(f"Commit created in the pull request: {commit_message}")
        else:
            print("Failed to create a commit in the pull request.")
    else:
        print("Failed to create a pull request.")


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

        # Create the modified file content
        modified_file_content = '\n'.join(valid_tokens)

        # Make a pull request with the modified file
        repo_owner = "TheLime1"
        repo_name = "gpt-cli"
        branch = "token_cleanup"
        title = "Token Cleanup"
        body = "This pull request removes bad tokens."
        file_path = "tokens/premium_tokens.txt"

        create_pull_request(repo_owner, repo_name, branch,
                            title, body, file_path, modified_file_content)

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
