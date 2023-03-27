

import openai


class GPTChatSession:
    def __init__(self, model="gpt-3.5-turbo", max_tokens=1000, n=1, stop=None, temperature=0.5):
        self.model = model
        self.max_tokens = max_tokens
        self.n = n
        self.stop = stop
        self.temperature = temperature
        self.history = []

    def chat(self, content, role="user"):
        self.history.append({"role": role, "content": content})
        # system role messages are not sent to the API for completion
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
            temperature=self.temperature
        )

        response_text = response.choices[0].message.content
        self.history.append({"role": "assistant", "content": response_text})
        return response_text

