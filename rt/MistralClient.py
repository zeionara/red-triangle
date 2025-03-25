from os import getenv
from requests import post
from json import loads, JSONDecodeError
from threading import Thread, Lock
from time import sleep

from .Client import Client, MessageHistory, Agent
from .util import ask_to_generate_concise_response
from .OpenChatClient import encode_agent


DEFAULT_MODEL = 'mistral-large-latest'
TIMEOUT = 3600


class MistralClient(Client):
    host = 'api.mistral.ai'

    def __init__(self, model: str, api_key: str, concise: bool = False, timeout: int = 3):
        super().__init__()

        self.concise = concise

        self.model = model
        self.api_key = api_key
        self.timeout = timeout

        self.headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

    @property
    def url(self):
        return f'https://{self.host}/v1/chat/completions'

    def ask(self, history: MessageHistory):
        messages = [
            {
                'role': encode_agent(message.agent),
                'content': message.text
            }
            for message in history
        ]

        # if self.concise:
        #     first_message = messages[0]
        #     first_message['content'] = ask_to_generate_concise_response(first_message['content'])

        last_user_message = None
        i = 0
        for message in history:
            if message.agent == Agent.USER:
                last_user_message_index = i
            i += 1

        last_user_message = messages[last_user_message_index]
        last_user_message['content'] = f'{last_user_message["content"]} Не используй markdown форматирование'

        response = post(
            self.url,
            headers = self.headers,
            json = {
                'model': self.model,
                'messages': messages,
                'stream': True
            },
            timeout = TIMEOUT,
            stream = True
        )
        lock = Lock()
        collected_output = ""

        def stream_worker():
            nonlocal collected_output

            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        decoded_line = line.decode('utf-8')
                        if decoded_line.strip() == "data: [DONE]":
                            break
                        if decoded_line.startswith("data:"):
                            decoded_line = decoded_line[len("data:"):].strip()
                        try:
                            data = loads(decoded_line)
                            delta = data.get("choices", [{}])[0].get("delta", {})
                            if "content" in delta:
                                text = delta["content"]

                                with lock:
                                    collected_output += text

                                print(text, end="")  # Optionally print text as it comes in
                        except JSONDecodeError:
                            continue
            else:
                response.raise_for_status()

            history.items[-1].text = collected_output
            print('\nCOMPLETED')

            # Wait for 3 seconds after streaming finishes
            # time.sleep(3)
            # Push the final collected text into the history object
            # history.push(collected_output)

        thread = Thread(target = stream_worker, daemon = True)
        thread.start()

        sleep(self.timeout)

        with lock:
            return collected_output

        # if response.status_code == 200:
        #     collected_output = ""
        #     # Iterate over the streamed response line by line
        #     for line in response.iter_lines():
        #         if line:
        #             # Decode the line and remove the "data: " prefix
        #             decoded_line = line.decode('utf-8')
        #             # Sometimes the stream sends a "data: [DONE]" message to indicate the end.
        #             if decoded_line.strip() == "data: [DONE]":
        #                 break
        #             # Remove the "data:" prefix if present
        #             if decoded_line.startswith("data:"):
        #                 decoded_line = decoded_line[len("data:"):].strip()
        #             try:
        #                 data = loads(decoded_line)
        #                 # The response is typically structured with a "choices" list that contains a "delta" dict.
        #                 delta = data.get("choices", [{}])[0].get("delta", {})
        #                 if "content" in delta:
        #                     text = delta["content"]
        #                     collected_output += text
        #                     print(text, end="")  # Print text as it comes in
        #             except json.JSONDecodeError:
        #                 # Handle lines that aren't valid JSON
        #                 continue
        #     # Return the complete collected message
        #     return collected_output
        # else:
        #     # You might want to handle non-200 responses
        #     response.raise_for_status()

        # if response.status_code == 200:
        #     return response.json()['choices'][0]['message']['content']

        # return response.text

    @classmethod
    def make(cls, model: str = None, concise: bool = False):
        if model is None:
            model = DEFAULT_MODEL

        return cls(model, getenv('MISTRAL_API_KEY'), concise = concise)
