from azure.authorization import AuthorizationDto
from azure.azure_http_client import AzureHttpClient


class InventoryCreator(object):

    def __init__(self, client: AzureHttpClient, subscription_id: str, resource_group_name: str) -> str:
        super().__init__()
        self.client = client
        self.resource_group_name = resource_group_name
        self.subscription_id = subscription_id

    def create(self, authorizationDto: AuthorizationDto):
        token = self.client.getAuthorizationToken(authorizationDto)
        ips = dict((self.__format(ip), self.client.getAzurePublicIp(token, self.subscription_id, self.resource_group_name, ip))
             for ip in self.client.getAzurePublicIps(token, self.subscription_id, self.resource_group_name))

        lbs = dict((self.__format(lb), self.client.getAzureLoadBalancerNatPool(token, self.subscription_id,
            self.resource_group_name, lb)) for lb in self.client.getAzureLoadBalancers(token, self.subscription_id, self.resource_group_name))

        inventory = ''
        for item in ips:
            inventory += f'[{item}s]\n'
            if item in lbs:
                i = 1
                for port in lbs[item]:
                    inventory += f'{item}{i} ansible_host={ips[item]} ansible_port={port}\n'
                    i += 1
            else:
                inventory += f'{item} ansible_host={ips[item]} ansible_port=22\n'
        return inventory

    @staticmethod
    def __format(azure_resource_name: str):
        return azure_resource_name.split('_')[0]