from abc import abstractmethod, ABC
from threading import RLock

from .Client import Client, MessageHistory
from .Agent import Agent


class Handler(ABC):
    def __init__(self, client: Client, agent: Agent = None):
        self.client = client
        self.agent = agent
        self.agent_lock = RLock()

    @abstractmethod
    def get_user(self, request: dict):
        pass

    @abstractmethod
    def get_utterance(self, request: dict):
        pass

    @abstractmethod
    def make_response(self, request: dict, message: str, end_session: bool = False):
        pass

    def is_stop(self, utterance: str):
        return 'стоп' in utterance

    def is_init(self, utterance: str):
        return 'навык' in utterance or 'скилл' in utterance or 'skill' in utterance

    def is_help(self, utterance: str):
        return 'можешь' in utterance or 'умеешь' in utterance or 'помощь' in utterance

    def has_skill_keyword(self, utterance: str):
        return 'skill' in utterance or 'скилл' in utterance

    def handle(self, request: dict, history: MessageHistory, chat: str = None):
        utterance = self.get_utterance(request)

        if self.is_stop(utterance):
            if self.agent is not None:
                with self.agent_lock:
                    self.agent.new_chat()

            return self.make_response(request, 'Завершаю сессию', end_session = True)
        if self.is_init(utterance):
            return self.make_response(request, 'Задайте ваш вопрос, а я постараюсь на него ответить')
        if self.is_help(utterance):
            return self.make_response(request, 'Я могу побеседовать с вами на любую тему, просто задайте вопрос')

        if self.agent is None:
            return self.make_response(request, self.client.ask(history))

        with self.agent_lock:
            if chat is None:
                if self.agent.chat is not None:
                    self.agent.new_chat()
            else:
                self.agent.to_chat(chat)

            return self.make_response(request, self.agent.ask(utterance))[0], self.agent.chat
