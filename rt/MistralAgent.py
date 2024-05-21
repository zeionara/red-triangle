from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys


class MistralAgent:
    def __init__(self, cookies: dict, response_wait_interval: int = 5, initialization_interval: int = 2, chat_initialization_interval: int = 1):
        self.cookies = cookies
        self.driver = webdriver.Chrome()

        self.response_wait_interval = response_wait_interval
        self.chat_initialization_interval = chat_initialization_interval
        self.initialization_interval = initialization_interval

        self.initialized = False
        self.has_chat = False

    def _submit(self, _textarea):
        button = self.driver.find_element(by = By.XPATH, value = "//button[@type='submit']")
        button.click()

        # textarea.send_keys(Keys.ENTER)

    def start(self, initial_prompt: str = 'hello, what can you do?'):
        if self.initialized:
            raise ValueError('The agent has already started')

        self.driver.get('https://mistral.ai')

        for key, value in self.cookies.items():
            cookie = {'name': key, 'value': value, 'domain': '.mistral.ai', 'path': '/'}
            self.driver.add_cookie(cookie)

        self.driver.get('https://chat.mistral.ai/chat')

        sleep(self.initialization_interval)

        if not self.initialized:
            self.initialized = True

    def ask(self, prompt: str):
        if not self.initialized:
            raise ValueError('The agent has not been started')

        textarea = self.driver.find_element(by = By.TAG_NAME, value = 'textarea')
        textarea.send_keys(prompt)

        if not self.has_chat:
            sleep(self.chat_initialization_interval)
            self.has_chat = True

        self._submit(textarea)
        sleep(self.response_wait_interval)

        messages = self.driver.find_elements(by = By.CLASS_NAME, value = 'prose-neutral')

        return messages[-1].text

    def new_chat(self):
        if not self.initialized:
            raise ValueError('The agent has not been started')

        self.has_chat = False
        self.driver.get('https://chat.mistral.ai/chat')

        sleep(self.initialization_interval)
