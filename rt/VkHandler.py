from .Handler import Handler


class VkHandler(Handler):

    def get_utterance(self, request: dict):
        request_body = request.get('request')

        if request_body is None:
            return None

        return request_body.get('command')

    def make_response(self, request: dict, message: str, end_session: bool = False):
        return {
            "response": {
                "text": message,
                "tts": message,
                "end_session": end_session
            },
            "session": request.get('session'),
            "version": request.get('version')
        }
