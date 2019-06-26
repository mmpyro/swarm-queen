from azure.authorization import AuthorizationDto
from azure.azure_http_client import AzureHttpClient


class InventoryCreator(object):

    def __init__(self, client: AzureHttpClient, subscription_id: str, resource_group_name: str) -> str:
        super().__init__()
        self.client = client
        self.resource_group_name = resource_group_name
        self.subscription_id = subscription_id
        self.inventory = None

    def create(self, authorizationDto: AuthorizationDto):
        self.inventory = ''
        token = self.client.getAuthorizationToken(authorizationDto)
        ips = dict((self.__format(ip), self.client.getAzurePublicIp(token, self.subscription_id, self.resource_group_name, ip))
             for ip in self.client.getAzurePublicIps(token, self.subscription_id, self.resource_group_name))

        lbs = dict((self.__format(lb), self.client.getAzureLoadBalancerNatPool(token, self.subscription_id,
            self.resource_group_name, lb)) for lb in self.client.getAzureLoadBalancers(token, self.subscription_id, self.resource_group_name))

        self._create_primal_master(ips, lbs)
        self._create_masters(ips, lbs)
        self._create_workers(ips, lbs)
        return self.inventory

    def _create_primal_master(self, ips: dict, lbs: dict) -> None:
        self.inventory += f'[primal_master]\n'
        if 'master' in lbs:
            self.inventory += f'master ansible_host={ips["master"]} ansible_port={lbs["master"][0]}\n'
        else:
            self.inventory += f'master ansible_host={ips["master"]} ansible_port=22\n'

    def _create_masters(self, ips: dict, lbs: dict) -> None:
        if 'master' in lbs and len(lbs['master']) > 1:
            i = 0
            self.inventory += f'[secondary_masters]\n'
            for port in lbs['master'][1:]:
                i += 1
                self.inventory += f'master{i} ansible_host={ips["master"]} ansible_port={port}\n'

    def _create_workers(self, ips: dict, lbs: dict) -> None:
        i = 0
        self.inventory += '[workers]\n'
        for port in lbs['worker']:
            i += 1
            self.inventory += f'worker{i} ansible_host={ips["worker"]} ansible_port={port}\n'

    @staticmethod
    def __format(azure_resource_name: str):
        return azure_resource_name.split('_')[0]