from .Handler import Handler


class SberHandler(Handler):

    def get_utterance(self, request: dict):
        payload = request.get('payload')

        if payload is None:
            return None

        message = payload.get('message')

        if message is None:
            return None

        return message.get('original_text')

    def make_response(self, request: dict, message: str, end_session: bool = False):
        payload = request.get('payload')

        return {
            'sessionId': request.get('sessionId'),
            'messageId': request.get('messageId'),
            'uuid': request.get('uuid'),
            'messageName': 'ANSWER_TO_USER',
            'payload': {
                'pronounceText': message,
                'pronounceTextType': 'application/text',
                'emotion': {
                    'emotionId': 'radost'
                },
                'auto_listening': not end_session,
                'finished': end_session,
                'device': payload.get('device')
            }
        }
