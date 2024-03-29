# Mudflap / GPTerminator / Karl's ChatGPT helpers

Sorry we don't have a good name yet.  We're workshopping it with gpt-4 but we're not rushing it.

## What is this noise?

It's a couple-three things.

1. chatgpt program for use in shell scripts, batch workflows, etc.  (Forty years of Unix is something one wants to embrace, not fight. -- Mark Diekhans)
2. gptshell - command-line tool for interacting with chatGPT that streams and saves.
3. Python package for interacting with the ChatGPT API that maintains session history to permit a context-maintaining dialog, loading, saving, etc.

## For any of this to work

You gotta have an OpenAI API key. Get one and set the `OPENAI_API_KEY` environment variable to have it, or use `openai api_key set <YOUR_API_KEY>`, or some other method to set your API key before proceeding.

## install

You can install the package from pypi using pip with

```
pip install karls_chatgpt_helpers
```

If you want to build from source, checkout the repo, do a `make build` and a `make install` or just say `python3 -m build` and `pip install .`

If you want to hack on this you might consider installing it with `pip3 install --editable .` then you can edit the python files in the repo and the changes will appear to your python programs (while in that environment or virtual environment) without having to rebuild and reinstall.  Check your friendly search engine or ask your AI assistant for details.

## The ChatGPT command line tool

'chatgpt' is a unix/linux/macos command line tool for use in normal automated Unix workflows, for example, shell scripts.

It can read prompts from stdin, command line arguments, a file, etc.  It has a robust set of command line arguments.

You can use it in a Unix pipeline where you pipe the output of a program into it and you pipe its output to another program.

A simple example use might be to translate and summarize the text of all the files in a certain directory, creating corresponding files in another directory.

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
echo "did mrs. o'leary's cow really kick over a lantern?" | chatgpt
```

```bash
chatgpt --system-prompt 'you are a computer expert and an expert russian translator' \
    'please give me a commented python code fragment to read the contents of stdin to a string variable, in russian'
```
```plaintext
# Этот код фрагмент считывает содержимое стандартного ввода в строковую переменную

import sys

# Читаем все введенные данные из стандартного ввода
input_data = sys.stdin.read()

# Выводим считанные данные на экран
print(input_data)

```

### system prompts and user prompts

A system prompt is designed to guide users or solicit specific information. It often sets the context for a conversation or interaction.

System prompts can be specified from the command line with the `--system-prompt` argument, followed by a system prompt string, and also from a file using `--system-prompt-file`.  If both are specified both are used, with the command line prompt sent before the prompt file.

A user prompt, on the other hand, is an input or question posed by an end-user to the model, seeking information, assistance, or a specific action. It reflects the user's needs or intentions.

User prompts can be specified from the command line in that whatever is on the command line that isn't a command line argument becomes the initial part of the user prompt.

If `--user-prompt-file` is specified, the named file is added to the user prompt.

Finally, if `--stdin` is specified or no user prompt file argument was specified and no user prompt argument was specified on the command line, stdin is read for the user prompt and added to any user prompt that already exists.

If no user prompt is specified, the program exits without producing any output.

If a user prompt is specified, the system prompts, if any, are sent to chatGPT, and the user prompt is sent, and the reply from the assistant is sent to stdout.


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


## gptshell

gptshell is an interactive program that solicits user input and enables an interactive conversation with ChatGPT.  You might think of it as a command line equivalent of the ChatGPT dialog page at https://chat.openai.com/.

We think the conversations people have with gpt-3.5, gpt-4, etc, for example when writing software, will be important pieces of documentation, the preserving of which may be valuable going foward.  For instance you might take a conversation you had with gpt-3.5, your pompts and its, and ask gpt-4 to look it over and see if it sees any bugs, oddities, or improvements in can make.  gpt-4 said it thinks this is a good idea.

When you fire up gptshell, you get a prompt:
```
gpt>
```

At this point you can type something and when you press enter it will be sent to OpenAI's chat completion API.  Like the webpage, the results will be streamed back.  If you decide you don't want to see the rest of the result, i.e. you want it to stop generating, hit control-C.

```bash
% gptshell
gpt> was basketball originally played with a wicker basket or something?
```
Yes, basketball was originally played with a peach basket or a woven wicker basket placed on a 10-foot-high pole. The game was invented by James Naismith in 1891, and the first basketball game was played with a soccer ball and two peach baskets as the goals. The baskets had no bottom, so players had to retrieve the ball after each score by climbing a ladder or using a stick to poke it out. The modern basketball hoop with a net was not introduced until the 1900s.
```
gpt> did they at one point have a pullstring to release the ball from the net?
```
Yes, basketball hoops with pullstrings to release the ball from the net were used in the early 1900s. The pullstring mechanism was invented by a Canadian physical education teacher named Dr. Luther Gulick in 1906. The design featured a cord attached to the bottom of the net that ran through a pulley system and down to the ground. When a player scored a basket, they could pull the cord to release the ball from the net without having to climb up and retrieve it. The pullstring mechanism was eventually replaced by a simpler design that used a metal ring attached to the bottom of the net to allow the ball to pass through.

Apparently you can get better answers if you provide some system prompts.  Like telling it it's an expert programmer before asking it coding questions.  Here's a possible example:

_You are an expert software developer. Functions should generally be limited to about 20 lines.  If longer, a subroutine should be factored.  If there is a function that processes many rows, like lines from a file, results from a SQLite SQL select, etc, and the function body is more than a few lines, factor a function that processes a single row and call it from the function that processes many rows.  The main function should handle command line arguments and set things up but it should call a function to do the work._

That's a bit of a pain to copy and paste every session, so you can specify a file containing a system prompt on the command line using `-s` or `--system-file`.

If the first character you enter at the command prompt is a percent sign, the percent sign is a command prefix that should be followed by one of our meta commands:

### gptshell meta commands

* %load filename - load a previous or pre-prepared conversation in RFC822 format.
* %save filename  - save the current conversation in RFC822 format.  This is preferred for human readability.
* %yload filename - load a previous or pre-prepared conversation in YAML format.
* %ysave filename - save a previous or pre-prepared conversation in YAML format.
* %jload filename - load a previous or pre-prepared conversation in JSON format.
* %jsave filename - save a previous or pre-prepared conversation in JSON format.

* %edit - go into your editor, edit, and if you save, sends what you saved as a user prompt.
* %sysedit - go into your editor, edit, and if you save, sends what you saved as a system prompt.
* %list - lists the conversation history, zero or more rows containing a role (user, system, or assistant) and content.
* %history - list the conversation history in a pleasing human-readable form.
* #! - execute remainder of input in a shell.  `#!bash` will create an interactive bash shell.  EOF will return you to gptshell.
* #interact - interactively enter the python interpreter that is currently running gptshell.  if you control-D you will be back in gptshell.

You can load and save conversations in RFC822, YAML and JSON.  RFC822 seems to be the best if you want to copy and paste stuff out of the replies, as it munges the text the least.  The yaml version doesn't come out looking particularly attractive, although it works.

You can specify a system prompt file on the command line, or you can edit something up in your editor with _%sysedit_.

You can specify prompts at the command line, but let's say you want to also tell GPT your SQL schema and your python class and your program before you ask your question.  Do _%edit_, then in your edit pull in your schema, your class, your program, and then write your actual prompts and the beginning and/or the end.  Something like "consider the below SQL schema, python class, and program, please add these new columns to the xxx table and propagate them through all the functions that reference elements of the table, or whatever.

### gptshell command line arguments

```
usage: gptshell [-h] [-s SYSTEM_FILE] [-i LOAD] [-w SAVE] [-m MODEL] [-t TEMPERATURE]

options:
  -h, --help            show this help message and exit
  -s SYSTEM_FILE, --system-file SYSTEM_FILE
                        the system prompt file to use
  -i LOAD, --load LOAD  load a session from a file
  -w SAVE, --save SAVE  save the session to a session file
  -m MODEL, --model MODEL
                        Model used for response generation
  -t TEMPERATURE, --temperature TEMPERATURE
                        Temperature for response generation
```

If you say `gptshell -load sesh -save sesh`, gptshell will read in the session and save it back out after you do what you do.

Model is gpt-3.5-turbo by default but can be set to gpt-4 if you have API access to gpt-4.

Temperature defaults to 0.7 but can be set higher or lower using the switches shown above.

## python package

Context-maintaining chatGPT session class

The thing where you have a conversation with ChatGPT and it has the context of what you've already been talking about as you say new things, the entire conversation is sent to the AI for each new user message.  (Sytem messages are recorded but aren't sent until there's also a user message, as system messages aren't replied to by the AI.)

Consequently if you're using the openai stuff directly, you have to do that.  GPTChatSession does that for you.  Any session can be saved or retrieved to a file, in either RFC-822, JSON or YAML format.

We find that RFC-822 is preferred because the reply text gets munged the least that way.  So if it gave you some source code or whatever, it's fit for copypasta without converstion, whereas multiline text gets sort of mangled when stored as JSON or YAML and requires conversion before use.

```python
import karls_chatgpt_helpers

g = karls_chatgpt_helpers.GPTChatSession()

reply = g.chat('Please give me a paragraph of gibberish so I can test my API.')
print(reply)

reply = g.chat('Another one, please.')
print(reply)

g.save('mysession.txt')

```

* g.chat(content) - append content to history as a user or system prompt (role='user' or 'system', default 'user') and send to open.ChatCompletion.create() and return the reply.
* g.streaming_chat(content) - same as chat except the output is streamed.  the chunks are written and flushed to stdout as they are received, as well as being accumulated into a reply content string.  When the entire response has been received, or a keyboard interrupt has occurred, the content string is appended to the history with the role set to 'assistant', and the assembled content string is returned.
* g.load(filename) - load a conversation in RFC822 format.
* g.save(filename) - save a conversation in RFC822 format.
* g.load_json(filename) - load a conversation in JSON format.
* g.save_json(filename) - save a conversation in JSON format.
* g.load_yaml(filename) - load a conversation in YAML format.
* g.save_yaml(filename) - save a conversation in YAML format.


### example

```python
import karls_chatgpt_helpers


    g = karls_chatgpt_helpers.GPTChatSession(
        model='gpt-3.5-turbo',
	max_tokens=1000,
	stop=None,
	temperature=0.5,
        debug=False
    )

    reply = g.chat("You think I'm a replicant, don't you?")

```

### Usage

```
gptshell [-h] [-s SYSTEM_FILE] [-i LOAD] [-m MODEL]

options:
  -h, --help            show this help message and exit
  -s SYSTEM_FILE, --system-file SYSTEM_FILE
                        the system prompt file to use
  -i LOAD, --load LOAD  load a file
  -m MODEL, --model MODEL
                        Model used for response generation
```
