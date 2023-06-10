import os
import pyperclip
from poefunc import delete_chat

ascii_art = '''
    __     _                        ______ __            __ 
   / /    (_)____ ___   ___        / ____// /_   ____ _ / /_
  / /    / // __ `__ \ / _ \      / /    / __ \ / __ `// __/
 / /___ / // / / / / //  __/     / /___ / / / // /_/ // /_  
/_____//_//_/ /_/ /_/ \___/______\____//_/ /_/ \__,_/ \__/  
                          /_____/                           
'''


def store_conversation(user_input, bot_response, bot_name, conversation):
    conversation.append((user_input, bot_response, bot_name))


def insert_clipboard_message():
    clipboard_text = pyperclip.paste()
    if clipboard_text:
        print("\nClipboard contents:\n")
        print(clipboard_text)
        print("\n")
        return clipboard_text


def export_conversation(conversation, ascii_art):
    filename = input("Enter the file name: ")
    filename += ".txt"
    directory = "conv"  # default name, you can change it
    if not os.path.exists(directory):
        os.makedirs(directory)
    filepath = os.path.join(directory, filename)
    with open(filepath, "w", encoding='utf-8') as file:
        file.write(ascii_art)
        for user_input, bot_response, bot_name in conversation:
            file.write("#######################\n")
            file.write(f"**USER**: {user_input}\n")
            file.write(f"**BOT**: {bot_response}\n")
        file.write("\n***conversation exported by limebot_cli***")
        file.close()
    print(f"Conversation exported to {filepath}.")


def print_menu():
    print("-" * 50)
    print("[1] - Change the bot (somtimes buggy)")
    print("[2] - Insert clipboard contents as message")
    print("[3] - Export conversation to .txt file")
    print("[0] - Close the program and delete chat history")
    print("\nType your message or choose an option:\n")


def change_bot():
    bot_input = input(
        "[1] - Sage (tweaked 3.5gpt_turbo) 4096 tokens\n[2] - ChatGPT (default) 4096 tokens\n[3] - GPT4(slower,more accurate) 8192 tokens \n[4] - Claude (default, FAST) 4500 tokens\n[5] - Claude+ (more creative, FASTER) 9000 tokens\n[6] - Claude_100K (BETA, very long messages) 100000 tokens\n[7] - Bard (very tight,better at programming) 4097 tokens\n[8] - Bing (different styles, can access the internet) 2000 tokens\n\nChoose your bot: ")
    if bot_input == "1":
        bot = "sage"
    elif bot_input == "2":
        bot = "chatgpt"
    elif bot_input == "3":
        bot = "gpt4"
    elif bot_input == "4":
        bot = "claude"
    elif bot_input == "5":
        bot = "claudeplus"
    elif bot_input == "6":
        bot = "claudehunk"
    elif bot_input == "7":
        bot = "bard"
    elif bot_input == "8":
        bot = "bing"
    else:
        print("Invalid input, please try again.")
    return bot


def close_program(current_premium_token):
    print("clearing chat history...")
    delete_chat(current_premium_token)
    pass
