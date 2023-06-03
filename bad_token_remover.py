import poe
import requests
import os
import base64
from datetime import datetime


def create_pull_request(repo_owner, repo_name, branch, title, body, file_path, file_content):
    headers = {
        "Authorization": f"Bearer {os.environ.get('G_TOKEN')}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Get the SHA of the most recent commit on the base branch
    base_branch = "main"
    base_branch_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/git/ref/heads/{base_branch}"
    response = requests.get(base_branch_url, headers=headers)
    if response.status_code == 200:
        base_branch_info = response.json()
        base_branch_sha = base_branch_info["object"]["sha"]
    else:
        print("Failed to get base branch info.")
        print(f"Status code: {response.status_code}")
        print(f"Response body: {response.text}")
        return

    # Generate a unique branch name by appending a timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique_branch = f"{branch}-{timestamp}"

    # Create a new branch with the updated file content
    new_branch_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/git/refs"
    new_branch_payload = {
        "ref": f"refs/heads/{unique_branch}",
        "sha": base_branch_sha
    }
    response = requests.post(
        new_branch_url, headers=headers, json=new_branch_payload)
    if response.status_code == 201:
        print(f"New branch created: {unique_branch}")
    else:
        print("Failed to create new branch.")
        print(f"Status code: {response.status_code}")
        print(f"Response body: {response.text}")
        return

    # Get the SHA of the most recent commit for the file
    file_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}?ref={unique_branch}"
    response = requests.get(file_url, headers=headers)
    if response.status_code == 200:
        file_info = response.json()
        file_sha = file_info["sha"]
    else:
        print("Failed to get file info.")
        print(f"Status code: {response.status_code}")
        print(f"Response body: {response.text}")
        return

    # Create a commit with the modified file in the new branch
    commit_message = f"Update {file_path}"
    commit_payload = {
        "message": commit_message,
        "content": file_content,
        "branch": unique_branch,
        "sha": file_sha
    }

    commit_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
    response = requests.put(
        commit_url, headers=headers, json=commit_payload)

    if response.status_code == 201:
        print(f"Commit created in the new branch: {commit_message}")
    else:
        print("Failed to create a commit in the new branch.")
        print(f"Status code: {response.status_code}")
        print(f"Response body: {response.text}")


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
        encoded_file_content = base64.b64encode(
            modified_file_content.encode('utf-8')).decode('utf-8')

        # Make a pull request with the modified file
        repo_owner = "TheLime1"
        repo_name = "gpt-cli"
        branch = "workflow-test"
        title = "Token Cleanup"
        body = "This pull request removes bad tokens."
        file_path = "tokens/premium_tokens.txt"

        create_pull_request(repo_owner, repo_name, branch,
                            title, body, file_path, encoded_file_content)

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
