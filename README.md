


## The ChatGPT command line tool

'chatgpt' is a command line tool for integrating into normal Unix workflow, for example, shell scripts.

It can read prompts from stdin and/or command line arguments.

### Examples

```bash
chatgpt 'what is the capital of texas'
```
```plaintext
The capital of Texas is Austin.
```

```bash
chatgpt what is the capital of indiana
```
```plaintext
The capital of Indiana is Indianapolis.
```

```bash
chatgpt --system-prompt 'you are a computer expert and an expert russian translator' 'please give me a commented python code fragment to read the contents of stdin to a string variable, in russian'
```
```plaintext
# Этот код фрагмент считывает содержимое стандартного ввода в строковую переменную

import sys

# Читаем все введенные данные из стандартного ввода
input_data = sys.stdin.read()

# Выводим считанные данные на экран
print(input_data)

```

A system prompt is designed to guide users or solicit specific information. It often sets the context for a conversation or interaction.

System prompts can be specified from the command line with the `--system-prompt` argument, followed by a system prompt string, and also from a file using `--system-prompt-file`.  If both are specified both are used, with the prompt sent first.

A user prompt, on the other hand, is an input or question posed by an end-user to the model, seeking information, assistance, or a specific action. It reflects the user's needs or intentions.

User prompts can be specified from the command line in that whatever is on the command line that isn't a command line argument becomes the initial part of the user prompt.

If `--user-prompt-file` is specified, the named file is added to the user prompt.

Finally, if `--stdin` is specified or no user prompt file was specified and no user prompt was specified on the command line, stdin is read for the user prompt and added to any user prompt that already exists.

If no user prompt is specified, the program exits.

If a user prompt is specified, it is sent to chatGPT and the reply from the assistant is sent to stdout.


### usage

usage: chatgpt [-h] [--system-prompt SYSTEM_PROMPT] [--system-prompt-file SYSTEM_PROMPT_FILE]
               [--user-prompt-file USER_PROMPT_FILE] [--temperature TEMPERATURE] [--max-tokens MAX_TOKENS]
               [--model MODEL] [--stdin]

ChatGPT shell command

options:
  -h, --help            show this help message and exit
  --system-prompt SYSTEM_PROMPT
                        System prompt content
  --system-prompt-file SYSTEM_PROMPT_FILE
                        File containing system prompt content
  --user-prompt-file USER_PROMPT_FILE
                        File containing user prompt content
  --temperature TEMPERATURE
                        Temperature for response generation
  --max-tokens MAX_TOKENS
                        Maximum tokens in generated response
  --model MODEL         Model used for response generation
  --stdin               Read prompt from standard input




context-maintaining chatGPT session class

```
import karls_chatgpt_helpers

g = karls_chatgpt_helpers.GPTChatSession()

g.chat('message')
g.chat('message', role='user')

g.chat('message', role='system')

```

