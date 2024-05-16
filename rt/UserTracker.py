from .Handler import Handler
from .Client import MessageHistory, Agent


class UserTracker:

    def __init__(self, handler: Handler):
        self.handler = handler
        self.histories = {}

    def handle(self, request: dict):
        handler = self.handler
        utterance = handler.get_utterance(request)

        user = handler.get_user(request)
        history = None
        is_not_init = None

        if handler.is_stop(utterance):
            self.histories.pop(user)
        else:
            if (history := self.histories.get(user)) is None:
                self.histories[user] = history = MessageHistory()

            if (is_not_init := (not handler.is_init(utterance) and not handler.is_help(utterance))):
                history.push(utterance)
                # print(history.describe())

        response, message = handler.handle(request, history)

        if history is not None and is_not_init:
            history.push(message, Agent.ASSISTANT)

        return response
