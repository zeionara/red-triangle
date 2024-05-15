from .Handler import Handler


class YandexHandler(Handler):

    def is_init(self, utterance: str):
        return super().is_init(utterance) or len(utterance) < 1

    def can_handle(self, request: dict):
        meta = request.get('meta')

        if meta is None:
            return False

        client_id = meta.get('client_id')

        if client_id is None:
            return False

        return 'yandex' in client_id

    def get_user(self, request: dict):
        session = request.get('session')

        if session is None:
            return None

        user = session.get('user')

        if user is None:
            return None

        return user.get('user_id')

    def get_utterance(self, request: dict):
        request_body = request.get('request')

        if request_body is None:
            return None

        return request_body.get('command')

    def make_response(self, request: dict, message: str, end_session: bool = False):
        response = {
            'response': {
                'text': message,
                'tts': message,
                'end_session': end_session,
            },
            "version": request.get('version')
        }

        state = request.get('state')

        if state is not None:
            if (session_state := state.get('session')) is not None:
                response['session_state'] = session_state

            if (user_state := state.get('user')) is not None:
                response['user_state_update'] = user_state

            if (application_state := state.get('application')) is not None:
                response['application_state'] = application_state

        return response
