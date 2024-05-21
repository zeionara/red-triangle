from time import sleep

from rt.MistralAgent import MistralAgent
from creds import mistral_cookies, mistral_target_chat

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
#
# driver = webdriver.Chrome()


def ask(agent_: MistralAgent, prompt: str):
    chat_before_asking = agent.chat

    print(f'> {prompt}')
    print()
    print(agent_.ask(prompt))
    print('-' * 50)

    if chat_before_asking is None and agent.chat is not None:
        print(f'(New chat: {agent.chat})')


agent = MistralAgent(mistral_cookies, response_wait_interval = 20).start()

ask(agent, 'what are the best comedy movies of 2014')
ask(agent, 'what about horror films?')

# agent.new_chat()
agent.to_chat(mistral_target_chat)

ask(agent, 'how to choose a toothbrush')
ask(agent, 'what about toothpaste?')

# driver.get('https://mistral.ai')
#
# for key, value in cookies.items():
#     cookie = {'name': key, 'value': value, 'domain': '.mistral.ai', 'path': '/'}
#     driver.add_cookie(cookie)
#
# driver.get('https://chat.mistral.ai/chat')
#
# sleep(2)
#
# textarea = driver.find_element(by = By.TAG_NAME, value = 'textarea')
# textarea.send_keys('hi, how are you?')
#
# sleep(1)
#
# textarea.send_keys(Keys.ENTER)
#
# sleep(5)
#
# messages = driver.find_elements(by = By.CLASS_NAME, value = 'prose-neutral')
#
# for message in messages:
#     print(message.text)

while True:
    sleep(5)
