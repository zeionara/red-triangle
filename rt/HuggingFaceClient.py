from os import environ as env

from requests import post


class HuggingFaceClient:
    def __init__(self, model: str, token: str):
        self.model = model
        self.token = token

    def ask(self, message: str):
        response = post(
            self.url,
            headers = self.headers,
            json = {
                'inputs': message
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
