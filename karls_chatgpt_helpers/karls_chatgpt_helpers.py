

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

    def chat(self, content, role="user"):
        '''Accept a string and an optional role.  if the role
        is "user" (default), the string is sent to the API for
        completion.  If the role is "system", the string is
        appended to the history without being sent to the API.

        the entire session history is sent, including of course
        the new prompt'''

        self.history.append({"role": role, "content": content})
        # system role messages are not sent to the API for completion
        if role == "system":
            return None
        elif role != "user":
            raise ValueError("role must be 'user' or 'system'")
        
        # send all the history to the API for completion
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.history,
            max_tokens=self.max_tokens,
            n=self.n,
            stop=self.stop,
            temperature=self.temperature
        )

        # dig out the response, append it to the history, and return it
        response_text = response.choices[0].message.content
        self.history.append({"role": "assistant", "content": response_text})
        return response_text

    def save(self, filename):
        '''Save the history to a file.'''
        with open(filename, "w") as f:
            json.dump(self.history, f)

    def load(self, filename):
        '''Load the history from a file.'''
        with open(filename, "r") as f:
            self.history = json.load(f)

