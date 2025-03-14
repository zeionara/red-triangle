from flask import Flask, request

from .Client import ClientType
from .Agent import AgentType
from .ClientFactory import ClientFactory
from .AgentFactory import AgentFactory

from .UserTracker import UserTracker
from .VkHandler import VkHandler
from .SberHandler import SberHandler
from .YandexHandler import YandexHandler


DEFAULT_HTTP_PORT = 1217
DEFAULT_HTTPS_PORT = 443


class Server:
    def __init__(
        self, model: str = None, client: ClientType = ClientType.HUGGINGFACE, agent: AgentType = None, concise: bool = False, collection: str = None,
        ssl_key: str = None, ssl_cert: str = None
    ):
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

        if ssl_cert and not ssl_key or not ssl_cert and ssl_key:
            raise ValueError('Both ssl key and ssl cert must be provided')

        self.ssl_key = ssl_key
        self.ssl_cert = ssl_cert

    @property
    def ssl_context(self):
        if self.ssl_cert is None or self.ssl_key is None:
            return None

        return (self.ssl_cert, self.ssl_key)

    def serve(self, host = '0.0.0.0', port = None):
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

        app.run(host = host, port = DEFAULT_HTTP_PORT if port is None and self.ssl_context is None else DEFAULT_HTTPS_PORT if port is None else port, ssl_context = self.ssl_context)
