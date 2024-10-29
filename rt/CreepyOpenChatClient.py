from os import environ as env
from random import randint

from requests import post

from .OpenChatClient import DEFAULT_MODEL, TIMEOUT
from .Client import Client, MessageHistory


def make_prompt_for_generating_introduction(story: str, concise: bool = False):
    if concise:
        return (
            'Придумай очень короткое введение к следующей истории на русском языке. '
            'Начни издалека и скажи, что ты собираешься рассказать пользователю интересную и жуткую историю, '
            f'но не пересказывай ее содержание, а только сошлись на основную идею. Текст истории: "{story}", '
            'Пример хорошего введения: "Присаживайся поудобнее, дорогой друг, и завари себе чайку, я расскажу тебе историю о маленьком мальчике, '
            'которого хотел убить могущественный маг, но в дело вмешались потусторонние силы"'
        )

    return f'Придумай введение к следующей истории. Во введении красиво скажи, что ты расскажешь пользователю интересную и жуткую историю, а также опиши ее содержание без раскрытия самых интересных деталей: {story}'


class CreepyOpenChatClient(Client):
    def __init__(self, model: str, host: str, port: int, stories_path: str = 'stories.txt', concise: bool = False):
        super().__init__()

        self.host = host
        self.port = port
        self.concise = concise

        with open(stories_path, 'r', encoding = 'utf-8') as file:
            stories = file.read().split('\n')

        stories = stories[:-1]

        self.stories = stories
        self.n_stories = len(stories)

        self.model = model

    @property
    def url(self):
        return f'http://{self.host}:{self.port}/v1/chat/completions'

    def ask(self, _history: MessageHistory):
        story_index = randint(0, self.n_stories - 1)
        story = self.stories[story_index]

        messages = [
            {'role': 'user', 'content': make_prompt_for_generating_introduction(story, concise = self.concise)}
        ]

        response = post(
            self.url,
            json = {
                'model': self.model,
                'messages': messages
            },
            timeout = TIMEOUT
        )

        return response.json()['choices'][0]['message']['content'] + '\n\n' + story

    @classmethod
    def make(cls, model: str = None, stories_path: str = 'stories.txt', concise: bool = False):
        if model is None:
            model = DEFAULT_MODEL

        return cls(model, host = env.get('OPENCHAT_HOST'), port = int(env.get('OPENCHAT_PORT')), stories_path = stories_path, concise = concise)
