from abc import abstractmethod, ABC


class Client(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def ask(self, message: str) -> str:
        pass
