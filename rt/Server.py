from flask import Flask, request

from .Client import ClientType
from .ClientFactory import ClientFactory

from .UserTracker import UserTracker
from .VkHandler import VkHandler
from .SberHandler import SberHandler
from .YandexHandler import YandexHandler


DEFAULT_PORT = 1217


class Server:
    def __init__(self, model: str = None, client: ClientType = ClientType.HUGGINGFACE):
        self.app = app = Flask('Red triangle')
        app.json.ensure_ascii = False

        self.client = client = ClientFactory.make(client, model)

        self.vk = UserTracker(VkHandler(client))
        self.sber = UserTracker(SberHandler(client))
        self.yandex = UserTracker(YandexHandler(client))

    def serve(self, host = '0.0.0.0', port = DEFAULT_PORT):
        app = self.app

        def handle(tracker: UserTracker):
            request_json = request.json
            utterance = tracker.handler.get_utterance(request_json)

            print(f'Got utterance "{utterance}" from user "{tracker.handler.get_user(request_json)}"')

            return tracker.handle(request_json)

        @app.route('/', methods = ['POST'])
        def ask_vk_and_yandex():
            if self.yandex.handler.can_handle(request.json):
                utterance = self.yandex.handler.get_utterance(request.json)

                if utterance == 'ping':
                    response, _ = self.yandex.handler.make_response(request.json, '')
                    return response

                return handle(self.yandex)

            return handle(self.vk)

        @app.route('/app-connector', methods = ['POST'])
        def ask_sber():
            return handle(self.sber)

        app.run(host = host, port = port)
