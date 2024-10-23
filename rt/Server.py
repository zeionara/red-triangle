from flask import Flask, request

from .Client import ClientType
from .Agent import AgentType
from .ClientFactory import ClientFactory
from .AgentFactory import AgentFactory

from .UserTracker import UserTracker
from .VkHandler import VkHandler
from .SberHandler import SberHandler
from .YandexHandler import YandexHandler


DEFAULT_PORT = 1217


class Server:
    def __init__(self, model: str = None, client: ClientType = ClientType.HUGGINGFACE, agent: AgentType = None, concise: bool = False, collection: str = None):
        self.app = app = Flask('Red triangle')
        app.json.ensure_ascii = False

        if agent is None:
            self.client = client = ClientFactory.make(client, model, concise = concise, collection = collection)
            self.agent = agent = None
        else:
            if concise:
                raise NotImplementedError('Concise option is not supported for agents')

            self.client = client = None
            self.agent = agent = AgentFactory.make(agent, response_wait_interval = 2).start()

        self.vk = UserTracker(VkHandler(client, agent))
        self.sber = UserTracker(SberHandler(client, agent))
        self.yandex = UserTracker(YandexHandler(client, agent))

    def serve(self, host = '0.0.0.0', port = DEFAULT_PORT):
        app = self.app

        def handle(tracker: UserTracker):
            request_json = request.json
            utterance = tracker.handler.get_utterance(request_json)

            print(f'Got utterance "{utterance}" from user "{tracker.handler.get_user(request_json)}"')

            response = tracker.handle(request_json)

            return response

        @app.route('/', methods = ['POST'])
        def ask_vk_and_yandex():
            if self.yandex.handler.can_handle(request.json):
                response, _ = self.yandex.handler.make_response(request.json, 'Ведутся технические работы, попробуйте позже')
                return response

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
