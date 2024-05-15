from click import group, argument, option, Choice

from .HuggingFaceClient import HuggingFaceClient
from .OpenAIClient import OpenAIClient
from .Server import Server
from .Client import ClientType, MessageHistory


@group()
def main():
    pass


@main.command()
@argument('message', type = str)
@option('--model', type = str)
@option('--client', type = Choice([client.value for client in ClientType], case_sensitive = False), default = ClientType.HUGGINGFACE.value)
def ask(message: str, model: str, client: str):
    match ClientType(client):
        case ClientType.HUGGINGFACE:
            client = HuggingFaceClient.make(model = model)
        case ClientType.OPENAI:
            client = OpenAIClient.make(model = model)
        case client_type:
            raise ValueError(f'Unknown client type: {client_type}')

    print(client.ask(MessageHistory().push(message)))


@main.command()
@option('--model', type = str)
@option('--client', type = Choice([client.value for client in ClientType], case_sensitive = False), default = ClientType.HUGGINGFACE.value)
def serve(model: str, client: str):
    Server(model, ClientType(client)).serve()


if __name__ == '__main__':
    main()
