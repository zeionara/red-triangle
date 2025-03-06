from os import getenv
from requests import post

from .Client import Client, MessageHistory
from .util import ask_to_generate_concise_response
from .OpenChatClient import encode_agent


DEFAULT_MODEL = 'mistral-large-latest'
TIMEOUT = 3600


class MistralClient(Client):
    host = 'api.mistral.ai'

    def __init__(self, model: str, api_key: str, concise: bool = False):
        super().__init__()

        self.concise = concise

        self.model = model
        self.api_key = api_key

        self.headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

    @property
    def url(self):
        return f'https://{self.host}/v1/chat/completions'

    def ask(self, history: MessageHistory):
        messages = [
            {
                'role': encode_agent(message.agent),
                'content': message.text
            }
            for message in history
        ]

        if self.concise:
            first_message = messages[0]
            first_message['content'] = ask_to_generate_concise_response(first_message['content'])

        response = post(
            self.url,
            headers = self.headers,
            json = {
                'model': self.model,
                'messages': messages
            },
            timeout = TIMEOUT
        )

        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']

        return response.text

    @classmethod
    def make(cls, model: str = None, concise: bool = False):
        if model is None:
            model = DEFAULT_MODEL

        return cls(model, getenv('MISTRAL_API_KEY'), concise = concise)
