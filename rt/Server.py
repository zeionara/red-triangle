from flask import Flask, request

from .HuggingFaceClient import HuggingFaceClient

from .Handler import Handler
from .VkHandler import VkHandler
from .SberHandler import SberHandler


class Server:
    def __init__(self, model: str):
        self.app = app = Flask('Red triangle')
        app.json.ensure_ascii = False

        self.client = client = HuggingFaceClient.make(model = model)

        self.vk = VkHandler(client)
        self.sber = SberHandler(client)

    def serve(self, host = '0.0.0.0', port = 1217):
        app = self.app

        def handle(handler: Handler):
            request_json = request.json
            utterance = handler.get_utterance(request_json)

            print(f'Got user utterance: "{utterance}"')

            return handler.handle(request_json)

        @app.route('/', methods = ['POST'])
        def ask_vk():
            return handle(self.vk)

        @app.route('/app-connector', methods = ['POST'])
        def ask_sber():
            return handle(self.sber)

        app.run(host = host, port = port)
