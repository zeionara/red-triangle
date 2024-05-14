from flask import Flask, request

from .HuggingFaceClient import HuggingFaceClient


class Server:
    def __init__(self, model: str):
        self.app = app = Flask(__name__)
        app.json.ensure_ascii = False

        self.client = HuggingFaceClient.make(model = model)

    def start(self, host = '0.0.0.0', port = 1217):
        app = self.app

        @app.route('/', methods = ['POST'])
        def ask():
            request_json = request.json

            request_body = request_json['request']
            text = request_body['command']

            print(f'Got text "{text}"')

            if 'стоп' in text:
                response = 'Завершаю сессию'
                end_session = True
            elif 'навык' in text:
                response = 'Задайте ваш вопрос, а я постараюсь на него ответить'
                end_session = False
            else:
                response = self.client.ask(text)
                end_session = False

            result = {
                "response": {
                    "text": response,
                    "tts": response,
                    "end_session": end_session
                },
                "session": request_json.get('session'),
                "version": request_json.get('version')
            }

            print(result)

            return result

        app.run(host = host, port = port)
