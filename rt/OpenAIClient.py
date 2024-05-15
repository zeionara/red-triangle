from os import environ as env

from openai import OpenAI

from .Client import Client, MessageHistory, Agent


DEFAULT_MODEL = 'gpt-3.5-turbo'


def encode_agent(agent: Agent):
    if agent == Agent.ASSISTANT:
        return 'assistant'

    if agent == Agent.USER:
        return 'user'

    raise ValueError(f'Incorrect agent: {agent.value}')


class OpenAIClient(Client):
    def __init__(self, model: str, token: str):
        super().__init__()

        self.model = model
        self.token = token
        self.client = OpenAI(token)

    def ask(self, history: MessageHistory):
        completion = self.client.chat.completions.create(
            model = self.model,
            messages = [
                {'role': encode_agent(message.agent), 'content': message.text}
                for message in history
            ]
        )

        return completion.choices[0].message

    @classmethod
    def make(cls, model: str = None):
        if model is None:
            model = DEFAULT_MODEL

        return cls(model, token = env.get('OPENAI_API_KEY'))
