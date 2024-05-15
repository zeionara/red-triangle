from os import environ as env

from requests import post

from .Client import Client, MessageHistory


class HuggingFaceClient(Client):
    def __init__(self, model: str, token: str):
        super().__init__()

        self.model = model
        self.token = token

    def ask(self, history: MessageHistory):
        print(history.describe())

        response = post(
            self.url,
            headers = self.headers,
            json = {
                'inputs': history.last_utterance
            }
        )

        if response.status_code == 200:
            return response.json()[0].get('generated_text')

        return response.json()

    @classmethod
    def make(cls, model: str):
        return cls(model, token = env.get('HUGGING_FACE_INFERENCE_API_TOKEN'))

    @property
    def url(self):
        return f'https://api-inference.huggingface.co/models/{self.model}'

    @property
    def headers(self):
        return {
            'Authorization': f'Bearer {self.token}'
        }
