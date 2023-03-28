
import argparse
import json
import os
import readline
import requests
import tempfile
import time

import openai

import karls_chatgpt_helpers

PROMPT = "gpt> "

def run_editor():
    editor = os.environ.get('EDITOR', 'vi')
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmpfile:
        tmpfile.close()  # close the file so that the editor can open it
        # open the file in the user's preferred editor
        os.system(f'{editor} {tmpfile.name}')
        if os.path.exists(tmpfile.name):
            # read the contents of the temporary file
            with open(tmpfile.name, 'r') as f:
                contents = f.read()
            # delete the temporary file
            os.unlink(tmpfile.name)
            return contents.strip()
        else:
            return ''


def converse(session_file):
    g = karls_chatgpt_helpers.GPTChatSession()

    # Prompt the user for input in a loop
    while True:
        try:
            role = 'user'
            print()
            line = input(PROMPT)
            print()

            if line.startswith('%list'):
                print(g.history)
                continue

            if line.startswith('%edit') or line.startswith('%sysedit'):
                role = 'system' if line.startswith('%sysedit') else 'user'
                # call the run_editor function to edit the input
                line = run_editor()

            if line.startswith('%'):
                print('Unknown command')
                continue

            if line.startswith('s:'):
                role = 'system'
                line = line[2:]

            if line == '':
                continue

            # Send the user input to ChatGPT
            g.streaming_chat(line, role=role)
        except EOFError:
            g.save(session_file)
            break
        except KeyboardInterrupt:
            print('interrupt')
            break




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('session_file', help='the session file to use')
    args = parser.parse_args()

    converse(args.session_file)


if __name__ == "__main__":
    main()
