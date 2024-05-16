from click import group, argument, option, Choice


from .Server import Server, DEFAULT_PORT
from .Client import ClientType, MessageHistory
from .ClientFactory import ClientFactory


@group()
def main():
    pass


@main.command()
@argument('message', type = str)
@option('-m', '--model', type = str)
@option('-c', '--client', type = Choice([client.value for client in ClientType], case_sensitive = False), default = ClientType.HUGGINGFACE.value)
def ask(message: str, model: str, client: str):
    print(
        ClientFactory.make(ClientType(client), model).ask(
            MessageHistory().push(message)
        )
    )


@main.command()
@option('-m', '--model', type = str)
@option('-c', '--client', type = Choice([client.value for client in ClientType], case_sensitive = False), default = ClientType.HUGGINGFACE.value)
@option('-p', '--port', type = int, default = DEFAULT_PORT)
def serve(model: str, client: str, port: int):
    Server(model, ClientType(client)).serve(port = port)


if __name__ == '__main__':
    main()
