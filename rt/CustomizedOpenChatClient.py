from os import environ as env

from requests import post

from .Client import Client, MessageHistory
from .util import ask_to_generate_concise_response


TIMEOUT = 3600


class CustomizedOpenChatClient(Client):
    def __init__(self, host: str, port: int, concise: bool = False):
        super().__init__()

        self.host = host
        self.port = port
        self.concise = concise

    @property
    def url(self):
        return f'http://{self.host}:{self.port}/ask'

    def ask(self, history: MessageHistory):
        response = post(
            self.url,
            json = {
                'query': ask_to_generate_concise_response(history.last_utterance) if self.concise else history.last_utterance
            },
            timeout = TIMEOUT
        )

        return response.json()['response']

    @classmethod
    def make(cls, concise: bool = False):
        return cls(host = env.get('OPENCHAT_HOST'), port = int(env.get('OPENCHAT_PORT')), concise = concise)
