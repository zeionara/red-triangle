from .Client import ClientType

from .HuggingFaceClient import HuggingFaceClient
from .OpenAIClient import OpenAIClient
from .OpenChatClient import OpenChatClient
from .CustomizedOpenChatClient import CustomizedOpenChatClient


class ClientFactory:

    @staticmethod
    def make(client_type: ClientType, model: str = None):
        match client_type:
            case ClientType.HUGGINGFACE:
                return HuggingFaceClient.make(model = model)
            case ClientType.OPENAI:
                return OpenAIClient.make(model = model)
            case ClientType.OPENCHAT:
                return OpenChatClient.make(model = model)
            case ClientType.CUSTOMIZED_OPENCHAT:
                return CustomizedOpenChatClient.make()
            case client_type:
                raise ValueError(f'Unknown client type: {client_type}')
