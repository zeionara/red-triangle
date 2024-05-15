from flask import Flask, request

from .HuggingFaceClient import HuggingFaceClient

from .UserTracker import UserTracker
from .VkHandler import VkHandler
from .SberHandler import SberHandler
from .YandexHandler import YandexHandler


class Server:
    def __init__(self, model: str):
        self.app = app = Flask('Red triangle')
        app.json.ensure_ascii = False

        self.client = client = HuggingFaceClient.make(model = model)

        self.vk = UserTracker(VkHandler(client))
        self.sber = UserTracker(SberHandler(client))
        self.yandex = UserTracker(YandexHandler(client))

    def serve(self, host = '0.0.0.0', port = 1217):
        app = self.app

        def handle(tracker: UserTracker):
            request_json = request.json
            utterance = tracker.handler.get_utterance(request_json)

            print(f'Got utterance "{utterance}" from user "{tracker.handler.get_user(request_json)}"')

            return tracker.handle(request_json)

        @app.route('/', methods = ['POST'])
        def ask_vk_and_yandex():
            if self.yandex.handler.can_handle(request.json):
                return handle(self.yandex)

            return handle(self.vk)

        @app.route('/app-connector', methods = ['POST'])
        def ask_sber():
            return handle(self.sber)

        app.run(host = host, port = port)
