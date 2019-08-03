from azure.azure_config import AzureConfig
from swarm_config import SwarmConfig


class Configuration(object):
    def __init__(self, config :dict) -> None:
        super().__init__()
        self.__azure_config = AzureConfig(config)
        self.__swarm_config = SwarmConfig(config)

    @property
    def swarm(self):
        return self.__swarm_config

    @property
    def azure(self):
        return self.__azure_config