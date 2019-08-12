import time
from azure.authorization import AuthorizationDto
from azure.azure_http_client import AzureHttpClient
from configuration import Configuration


class InventoryCreator(object):

    def __init__(self, client: AzureHttpClient, config: Configuration) -> str:
        super().__init__()
        self.config = config
        self.client = client
        self.resource_group_name = config.azure.resource_group
        self.subscription_id = config.azure.subscription_id
        self.inventory = None

    def create(self, authorization_dto: AuthorizationDto):
        self.inventory = ''
        token = self.client.getAuthorizationToken(authorization_dto)
        ips = dict((self.__format(ip), self.client.getAzurePublicIp(token, self.subscription_id, self.resource_group_name, ip))
             for ip in self.client.getAzurePublicIps(token, self.subscription_id, self.resource_group_name))

        lbs = self.__fill_lb_dict(token)

        while not self.__validate_nat_ports(lbs):
            time.sleep(2)
            lbs = self.__fill_lb_dict(token)

        self.__create_primal_master(ips, lbs)
        self.__create_masters(ips, lbs)
        self.__create_workers(ips, lbs)
        return self.inventory

    def __fill_lb_dict(self, token: str) -> dict:
        return dict((self.__format(lb), self.client.getAzureLoadBalancerNatPool(token, self.subscription_id,
                                                                               self.resource_group_name, lb)) for lb in
                   self.client.getAzureLoadBalancers(token, self.subscription_id, self.resource_group_name))

    def __create_primal_master(self, ips: dict, lbs: dict) -> None:
        self.inventory += f'[primal_master]\n'
        if 'master' in lbs:
            self.inventory += f'master ansible_host={ips["master"]} ansible_port={lbs["master"][0]}\n'
        else:
            self.inventory += f'master ansible_host={ips["master"]} ansible_port=22\n'

    def __create_masters(self, ips: dict, lbs: dict) -> None:
        if 'master' in lbs and len(lbs['master']) > 1:
            i = 0
            self.inventory += f'[secondary_masters]\n'
            for port in lbs['master'][1:]:
                i += 1
                self.inventory += f'master{i} ansible_host={ips["master"]} ansible_port={port}\n'

    def __create_workers(self, ips: dict, lbs: dict) -> None:
        i = 0
        self.inventory += '[workers]\n'
        for port in lbs['worker']:
            i += 1
            self.inventory += f'worker{i} ansible_host={ips["worker"]} ansible_port={port}\n'

    def __validate_nat_ports(self, lbs :dict):
        if ('master' in lbs and len(lbs['master'])) > self.config.swarm.masters or len(lbs['worker']) > self.config.swarm.workers:
            return False
        return True

    @staticmethod
    def __format(azure_resource_name: str):
        return azure_resource_name.split('_')[0]