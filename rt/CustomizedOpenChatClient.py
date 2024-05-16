from os import environ as env

from requests import post

from .Client import Client, MessageHistory


TIMEOUT = 3600


class CustomizedOpenChatClient(Client):
    def __init__(self, host: str, port: int):
        super().__init__()

        self.host = host
        self.port = port

    @property
    def url(self):
        return f'http://{self.host}:{self.port}/ask'

    def ask(self, history: MessageHistory):
        response = post(
            self.url,
            json = {
                'query': history.last_utterance
            },
            timeout = TIMEOUT
        )

        return response.json()['response']

    @classmethod
    def make(cls):
        return cls(host = env.get('OPENCHAT_HOST'), port = int(env.get('OPENCHAT_PORT')))
