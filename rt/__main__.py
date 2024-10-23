from click import group, argument, option, Choice


from .Server import Server, DEFAULT_PORT

from .Client import ClientType, MessageHistory
from .ClientFactory import ClientFactory

from .Agent import AgentType
from .AgentFactory import AgentFactory


@group()
def main():
    pass


@main.command()
@argument('message', type = str)
@option('-m', '--model', type = str)
@option('-c', '--client', type = Choice([client.value for client in ClientType], case_sensitive = False), default = ClientType.HUGGINGFACE.value)
@option('-a', '--agent', type = Choice([agent.value for agent in AgentType], case_sensitive = True), default = None)
def ask(message: str, model: str, client: str, agent: str):
    if agent is None:
        response = ClientFactory.make(ClientType(client), model).ask(
            MessageHistory().push(message)
        )
    else:
        response = AgentFactory.make(AgentType(agent)).start().ask(message)

    print(response)


@main.command()
@option('-m', '--model', type = str)
@option('-c', '--client', type = Choice([client.value for client in ClientType], case_sensitive = False), default = ClientType.HUGGINGFACE.value)
@option('-a', '--agent', type = Choice([agent.value for agent in AgentType], case_sensitive = True), default = None)
@option('-p', '--port', type = int, default = DEFAULT_PORT)
@option('-s', '--concise', is_flag = True)
@option('-l', '--collection', type = str)
def serve(model: str, client: str, agent: str, port: int, concise: bool, collection: str):
    Server(model, ClientType(client), None if agent is None else AgentType(agent), concise = concise, collection = collection).serve(port = port)


if __name__ == '__main__':
    main()
