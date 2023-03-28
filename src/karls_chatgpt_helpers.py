

import openai
import json
import os


class GPTChatSession:
    def __init__(self, model="gpt-3.5-turbo", max_tokens=1000, n=1, stop=None, temperature=0.5):
        self.model = model
        self.max_tokens = max_tokens
        self.n = n
        self.stop = stop
        self.temperature = temperature
        self.history = []

    def save(self, filename):
        '''Save the history to a file.'''
        with open(filename, "w") as f:
            json.dump(self.history, f)

    def load(self, filename):
        '''Load the history from a file.'''
        with open(filename, "r") as f:
            self.history = json.load(f)

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
            streaming=streaming
        )
        return response

    def chat(self, content, role="user"):
        response = self._chat(content, role, streaming=False)
        response_text = response.choices[0].message.content
        self.history.append({"role": "assistant", "content": response_text})
        return response_text

    def streaming_chat(self, content, role="user"):
        response = self._chat(content, role, streaming=True)

        response_text = ""
        for chunk in response:
            chunk_text = chunk.choices[0].message.content
            response_text += chunk_text
            print(chunk_text, end='', flush=True)

        self.history.append({"role": "assistant", "content": response_text})
        return response_text

