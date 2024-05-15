from abc import abstractmethod, ABC

from .Client import Client


class Handler(ABC):
    def __init__(self, client: Client):
        self.client = client

    @abstractmethod
    def get_utterance(self, request: dict):
        pass

    @abstractmethod
    def make_response(self, request: dict, message: str, end_session: bool = False):
        pass

    def handle(self, request: dict):
        utterance = self.get_utterance(request)

        if 'стоп' in utterance:
            return self.make_response(request, 'Завершаю сессию', end_session = True)
        if 'навык' in utterance:
            return self.make_response(request, 'Задайте ваш вопрос, а я постараюсь на него ответить')

        return self.make_response(request, self.client.ask(utterance))
