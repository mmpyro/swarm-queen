import os


class SwarmConfig(object):
    def __init__(self, config :dict) -> None:
        super().__init__()
        swarm = config['swarm']
        self.__number_of_workers = swarm['numberOfMasters']
        self.__number_of_masters = swarm['numberOfWorkers']
        self.__sshKeyPath = swarm['sshKeyPath']
        self.__sshPrivateKeyName = swarm['sshPrivateKeyName']
        self.__user = swarm['vmUserName']

    @property
    def workers(self) -> int:
        return self.__number_of_workers

    @property
    def masters(self) -> int:
        return self.__number_of_masters

    @property
    def ssh_key_path(self):
        return self.__sshKeyPath

    @property
    def ssh_private_key_name(self):
        return self.__sshPrivateKeyName

    @property
    def user_name(self):
        return self.__user

    @property
    def ssh_private_key_full_name(self):
        return os.path.join(self.__sshKeyPath, self.__sshPrivateKeyName)
