from enum import Enum
from abc import ABC, abstractmethod


class AgentType(Enum):
    MISTRAL = 'mistral'


class Agent(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def ask(self, prompt: str):
        pass

    @abstractmethod
    def new_chat(self):
        pass

    @abstractmethod
    def to_chat(self, chat: str):
        pass
