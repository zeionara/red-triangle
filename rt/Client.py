from enum import Enum
from dataclasses import dataclass
from abc import abstractmethod, ABC


class ClientType(Enum):
    HUGGINGFACE = 'huggingface'
    OPENAI = 'openai'
    OPENCHAT = 'openchat'


class Agent(Enum):
    ASSISTANT = 'assistant'
    USER = 'user'


@dataclass
class Message:
    text: str
    agent: Agent

    def describe(self):
        return f'{"U" if self.agent == Agent.USER else "A"}: {self.text}'


class MessageHistory:

    def __init__(self):
        self.items = []

    def push(self, text: str, agent: Agent = Agent.USER):
        self.items.append(Message(text, agent))
        return self

    def describe(self):
        return '\n'.join(message.describe() for message in self.items)

    @property
    def last_utterance(self):
        utterance = None

        for message in self.items:
            if message.agent == Agent.USER:
                utterance = message.text

        return utterance

    def __iter__(self):
        return iter(self.items)


class Client(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def ask(self, history: MessageHistory) -> str:
        pass
