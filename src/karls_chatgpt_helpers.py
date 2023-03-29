

import openai
import json
import os
import sys
import yaml

def openai_api_key_set_or_die():
    if openai.api_key is None:
        print("Error:  OpenAI API key not set.  Please set the OPENAI_API_KEY environment variable, use 'openai api_key set <YOUR_API_KEY>', or some other method to set it before proceeding.")
        sys.exit(1)



class GPTChatSession:
    def __init__(self, model="gpt-3.5-turbo", max_tokens=1000, n=1, stop=None, temperature=0.5, debug=False):
        self.model = model
        self.max_tokens = max_tokens
        self.n = n
        self.stop = stop
        self.temperature = temperature
        self.debug = debug
        self.history = []

    def load(self, filename):
        '''Load the history from a file.'''
        with open(filename, "r") as f:
            self.history = json.load(f)

    def save(self, filename):
        '''Save the history to a json file.'''
        with open(filename, "w") as f:
            json.dump(self.history, f, indent=4)

    def load_yaml(self, filename):
        '''Load the history from a yaml file.'''
        with open(filename, "r") as f:
            self.history = yaml.safe_load(f)

    def save_yaml(self, filename):
        '''Save the history to a yaml file.'''
        with open(filename, "w") as f:
            # default_flow_style can be True, False or None,
            # True means the output will be a single line
            # False means the output will be multiline
            # None means the output will be multiline if the data is multiline
            # canonical can be True or False
            yaml.dump(self.history, f, default_flow_style=False, canonical=False)

    def _chat(self, content, role="user", streaming=False):
        self.history.append({"role": role, "content": content})
        if role == "system":
            return None
        elif role != "user":
            raise ValueError("role must be 'user' or 'system'")

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.history,
            max_tokens=self.max_tokens,
            n=self.n,
            stop=self.stop,
            temperature=self.temperature,
            stream=streaming
        )

        return response

    def chat(self, content, role="user"):
        response = self._chat(content, role, streaming=False)
        if role == 'system':
            return None
        response_text = response.choices[0].message.content
        self.history.append({"role": "assistant", "content": response_text})
        return response_text

    def streaming_chat(self, content, role="user"):
        response = self._chat(content, role, streaming=True)
        if role == 'system':
            return None

        response_text = ""
        try:
            for chunk in response:
                if self.debug:
                    print("chunk:", chunk)
                delta = chunk.choices[0].delta
                if 'content' in delta:
                    # append the new text to the response
                    chunk_text = delta['content']
                    response_text += chunk_text
                    print(chunk_text, end='', flush=True)
        except KeyboardInterrupt:
            print("Interrupted")

        self.history.append({"role": "assistant", "content": response_text})
        return response_text

