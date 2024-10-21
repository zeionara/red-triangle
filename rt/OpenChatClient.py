from os import environ as env

from requests import post

from .Client import Client, MessageHistory, Agent
from .util import ask_to_generate_concise_response


DEFAULT_MODEL = 'openchat_v3.2_gemma_new'
TIMEOUT = 3600

ENCODED_USER_AGENT = 'user'


def encode_agent(agent: Agent):
    if agent == Agent.ASSISTANT:
        return 'assistant'

    if agent == Agent.USER:
        return ENCODED_USER_AGENT

    raise ValueError(f'Incorrect agent: {agent.value}')


class OpenChatClient(Client):
    def __init__(self, model: str, host: str, port: int, concise: bool = False):
        super().__init__()

        self.host = host
        self.port = port
        self.concise = concise

        self.model = model

    @property
    def url(self):
        return f'http://{self.host}:{self.port}/v1/chat/completions'

    def ask(self, history: MessageHistory):
        messages = [
            {'role': encode_agent(message.agent), 'content': message.text}
            for message in history
        ]

        if self.concise:  # and 0 < len(messages) < 2:
            first_message = messages[0]
            first_message['content'] = ask_to_generate_concise_response(first_message['content'])

        # if self.concise:
        #     for message in messages[::-1]:
        #         if message['role'] == ENCODED_USER_AGENT:
        #             message['content'] = f'Коротко ответь на вопрос "{message["content"]}"'

        # print(messages)

        response = post(
            self.url,
            json = {
                'model': self.model,
                'messages': messages
            },
            timeout = TIMEOUT
        )

        return response.json()['choices'][0]['message']['content']

    @classmethod
    def make(cls, model: str = None, concise: bool = False):
        if model is None:
            model = DEFAULT_MODEL

        return cls(model, host = env.get('OPENCHAT_HOST'), port = int(env.get('OPENCHAT_PORT')), concise = concise)
