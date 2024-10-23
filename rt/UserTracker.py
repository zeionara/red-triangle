# from pyautogui import hotkey

from .Handler import Handler
from .Client import MessageHistory, Agent


def looks_like_url(message: str):
    return message.startswith('http')


class UserTracker:

    def __init__(self, handler: Handler):
        self.handler = handler
        self.histories = {} if handler.agent is None else None
        self.voice_channel_states = {}
        self.chats = None if handler.agent is None else {}

    def handle(self, request: dict):
        handler = self.handler
        utterance = handler.get_utterance(request)

        user = handler.get_user(request)

        # if handler.has_skill_keyword(utterance):
        #     # print('Connected to voice channel:', self.voice_channel_states.get(user))

        #     if not self.voice_channel_states.get(user):
        #         # print('connecting...')
        #         self.voice_channel_states[user] = True
        #         # hotkey('ctrl', 'shift', 'alt', 'a')
        #     else:
        #         # print('disconnecting...')
        #         self.voice_channel_states[user] = False
        #         # hotkey('ctrl', 'shift', 'alt', 'b')

        #     return handler.make_response(request, '', end_session = True)[0]

        history = None
        is_not_init = None

        if handler.is_stop(utterance):
            if handler.agent is None:
                self.histories.pop(user)
            else:
                self.chats.pop(user)
        elif handler.agent is None:
            if (history := self.histories.get(user)) is None:
                self.histories[user] = history = MessageHistory()

            if (is_not_init := (not handler.is_init(utterance) and not handler.is_help(utterance))):
                history.push(utterance)
                # print(history.describe())

        response, message = handler.handle(request, history, chat = None if handler.agent is None else self.chats.get(user))

        if handler.agent is not None and looks_like_url(message):
            self.chats[user] = message

        if history is not None and is_not_init:  # it is unnecessary to check if handler.agent is None here
            history.push(message, Agent.ASSISTANT)

        return response
