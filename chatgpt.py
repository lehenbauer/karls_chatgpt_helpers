#!/usr/bin/env python3

import argparse
import os
import sys
from karls_chatgpt_helpers import GPTChatSession


def handle_system_prompt_file(session, filename):
    with open(filename, 'r') as file:
        content = file.read()
    session.chat(content, role="system")


def main():
    parser = argparse.ArgumentParser(description="ChatGPT shell command")

    parser.add_argument('--system-prompt', type=str, help='System prompt content')
    parser.add_argument('--system-prompt-file', type=str, help='File containing system prompt content')
    parser.add_argument('--user-prompt-file', type=str, help='File containing user prompt content')
    parser.add_argument('--temperature', type=float, default=0.7, help='Temperature for response generation')
    parser.add_argument('--max-tokens', type=int, default=1000, help='Maximum tokens in generated response')
    parser.add_argument('--model', type=str, default="gpt-3.5-turbo", help='Model used for response generation')
    parser.add_argument('--stdin', action='store_true', default=False, help='Read prompt from standard input')

    args, remaining_args = parser.parse_known_args()

    if not os.environ.get('OPENAI_API_KEY'):
        print("Please set the OPENAI_API_KEY environment variable.")
        sys.exit(1)

    session = GPTChatSession(
        model=args.model,
        max_tokens=args.max_tokens,
        temperature=args.temperature
    )

    if args.system_prompt:
        session.chat(args.system_prompt, role="system")

    if args.system_prompt_file:
        handle_system_prompt_file(session, args.system_prompt_file)

    # If we have a user prompt file, start the prompt with it
    user_prompt = ''
    if args.user_prompt_file:
        with open(args.user_prompt_file, 'r') as file:
            user_prompt = file.read()

    # If they specified --stdin, read from stdin and
    # append it to the user prompt
    if args.stdin:
        stdin_prompt = sys.stdin.read()
        if (user_prompt != ''):
            user_prompt += '\n\n' + stdin_prompt
        else:
            user_prompt = stdin_prompt

    # if we have remaining command line args, append or set them to the user prompt
    if len(remaining_args) > 0:
        command_line_prompt = " ".join(remaining_args)
        if (user_prompt != ''):
            user_prompt += '\n\n' + command_line_prompt
        else:
            user_prompt = command_line_prompt


    response_text = session.chat(user_prompt, role="user")
    sys.stdout.write(response_text)
    sys.stdout.write('\n')


if __name__ == "__main__":
    main()
