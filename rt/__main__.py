from click import group, argument

from .HuggingFaceClient import HuggingFaceClient
from .Server import Server


# DEFAULT_MODEL = 'zlsl/l_erotic_kink_chat'
DEFAULT_MODEL = 'Qwen/Qwen1.5-0.5B'


@group()
def main():
    pass


@main.command()
@argument('message', type = str)
def ask(message: str):
    # client = HuggingFaceClient.make(model = 'Qwen/Qwen1.5-0.5B')
    client = HuggingFaceClient.make(model = DEFAULT_MODEL)
    print(client.ask(message))


@main.command()
@argument('model', type = str, default = DEFAULT_MODEL)
def serve(model: str):
    Server(model).serve()


if __name__ == '__main__':
    main()
