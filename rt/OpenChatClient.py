from os import environ as env

from requests import post

from .Client import Client, MessageHistory, Agent


DEFAULT_MODEL = 'openchat_3.5'
TIMEOUT = 3600


def encode_agent(agent: Agent):
    if agent == Agent.ASSISTANT:
        return 'assistant'

    if agent == Agent.USER:
        return 'user'

    raise ValueError(f'Incorrect agent: {agent.value}')


class OpenChatClient(Client):
    def __init__(self, model: str, token: str, host: str, port: int):
        super().__init__()

        self.host = host
        self.port = port

        self.model = model
        self.token = token

    @property
    def url(self):
        return f'http://{self.host}:{self.port}/v1/chat/completions'

    def ask(self, history: MessageHistory):
        response = post(
            self.url,
            json = {
                'model': self.model,
                'messages': [
                    {'role': encode_agent(message.agent), 'content': message.text}
                    for message in history
                ]
            },
            timeout = TIMEOUT
        )

        return response.json()['choices'][0]['message']['content']

    @classmethod
    def make(cls, model: str = None):
        if model is None:
            model = DEFAULT_MODEL

        return cls(model, token = env.get('OPENAI_API_KEY'), host = env.get('OPENCHAT_HOST'), port = int(env.get('OPENCHAT_PORT')))
