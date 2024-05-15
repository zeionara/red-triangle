from .Handler import Handler


class VkHandler(Handler):

    def get_user(self, request: dict):
        session = request.get('session')

        if session is None:
            return None

        application = session.get('application')

        if application is None:
            return None

        return application.get('application_id')

    def get_utterance(self, request: dict):
        request_body = request.get('request')

        if request_body is None:
            return None

        return request_body.get('command')

    def is_stop(self, utterance: str):
        return utterance == 'on_interrupt' or super().is_stop(utterance)

    def make_response(self, request: dict, message: str, end_session: bool = False):
        return {
            "response": {
                'commands': [
                    {
                        'type': 'TTS',
                        'text': message,
                        'tts': message,
                        'voice': 'vasilisa-hifigan'
                    }
                ],
                "end_session": end_session
            },
            "session": request.get('session'),
            "version": request.get('version')
        }, message
