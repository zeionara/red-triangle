from os import getenv
from random import randint

from requests import post

from .OpenChatClient import DEFAULT_MODEL, TIMEOUT, ENCODED_USER_AGENT, encode_agent
from .CreepyOpenChatClient import make_prompt_for_generating_introduction
from .Client import Client, MessageHistory


class CreepyMistralClient(Client):
    host = 'api.mistral.ai'

    def __init__(self, model: str, api_key: str, concise: bool = False, stories_path: str = 'stories.txt'):
        super().__init__()

        self.concise = concise

        self.model = model
        self.api_key = api_key

        self.headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        with open(stories_path, 'r', encoding = 'utf-8') as file:
            stories = file.read().split('\n')

        stories = stories[:-1]

        self.stories = stories
        self.n_stories = len(stories)

    def refine_introduction(self, introduction: str):
        prompt = (
            'Проверь следующий текст на орфографические, синтаксические, семантические и грамматические ошибки '
            f'и сделай его более грамотным, мистическим и загадочным, также удали из текста ссылки и спецсимволы: "{introduction}"'
        )

        response = post(
            self.url,
            headers = self.headers,
            json = {
                'model': self.model,
                'messages': [
                    {
                        'role': ENCODED_USER_AGENT,
                        'content': prompt
                    }
                ]
            },
            timeout = TIMEOUT
        )

        return response.json()['choices'][0]['message']['content']

    @property
    def url(self):
        return f'https://{self.host}/v1/chat/completions'

    def ask(self, history: MessageHistory):
        print(history.describe())
        if len(history) < 1:
            story_index = randint(0, self.n_stories - 1)
            story = self.stories[story_index]

            message = make_prompt_for_generating_introduction(story, concise = self.concise)

            messages = [
                {'role': ENCODED_USER_AGENT, 'content': message}
            ]
        else:
            messages = [
                {'role': encode_agent(message.agent), 'content': message.text}
                for message in history
            ]

        response = post(
            self.url,
            headers = self.headers,
            json = {
                'model': self.model,
                'messages': messages
            },
            timeout = TIMEOUT
        )

        if len(history) < 1:
            introduction = response.json()['choices'][0]['message']['content']
            # introduction = self.refine_introduction(response.json()['choices'][0]['message']['content'])

            return introduction + '\n\n' + story

        return response.json()['choices'][0]['message']['content']

    @classmethod
    def make(cls, model: str = None, stories_path: str = 'stories.txt', concise: bool = False):
        if model is None:
            model = DEFAULT_MODEL

        return cls(model, api_key = getenv('MISTRAL_API_KEY'), stories_path = stories_path, concise = concise)
