from creds import mistral_cookies

from .Agent import AgentType
from .MistralAgent import MistralAgent


class AgentFactory:

    @staticmethod
    def make(agent_type: AgentType, response_wait_interval: int = 5, initialization_interval: int = 2, chat_initialization_interval: int = 1):
        match agent_type:
            case AgentType.MISTRAL:
                return MistralAgent(
                    mistral_cookies,
                    response_wait_interval = response_wait_interval,
                    initialization_interval = initialization_interval,
                    chat_initialization_interval = chat_initialization_interval
                )
            case _:
                raise ValueError(f'Unknown agent type: {agent_type}')
