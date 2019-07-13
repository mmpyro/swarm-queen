import json

import pydash
import requests
from azure.authorization import AuthorizationDto


class AzureHttpClient(object):
    def __init__(self) -> None:
        super().__init__()

    def getAuthorizationToken(self, authorization :AuthorizationDto) -> str:
        login_url = f'https://login.microsoftonline.com/{authorization.tenant_id}/oauth2/token?api-version=1.0'
        content = {'grant_type': 'client_credentials', 'resource': 'https://management.core.windows.net/',
                   'client_id': authorization.client_id, 'client_secret': authorization.secret}
        res = requests.post(login_url, content, headers={'Content-type': 'application/x-www-form-urlencoded'})
        content = json.loads(res.text)
        return content['access_token']

    def getAzureLoadBalancers(self, token :str, subscription_id :str, resource_group_name :str) -> list:
        url = f'https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Network/loadBalancers?api-version=2018-11-01'
        res = requests.get(url, headers={'Authorization': f'Bearer {token}'})
        content = json.loads(res.text)
        return pydash.map_(content['value'], 'name')

    def getAzureLoadBalancerNatPool(self, token :str, subscription_id :str, resource_group_name :str, lb_name :str) -> list:
        url = f'https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Network/loadBalancers/{lb_name}?api-version=2018-11-01'
        res = requests.get(url, headers={'Authorization': f'Bearer {token}'})
        content = json.loads(res.text)
        ssh_rules = pydash.filter_(content['properties']['inboundNatRules'], lambda item: 'ssh' in item['name'])
        return pydash.map_(ssh_rules, 'properties.frontendPort')

    def getAzurePublicIps(self, token :str, subscription_id :str, resource_group_name :str) -> list:
        url = f'https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Network/publicIPAddresses?api-version=2018-11-01'
        res = requests.get(url, headers={'Authorization': f'Bearer {token}'})
        content = json.loads(res.text)
        return pydash.map_(content['value'], 'name')

    def getAzurePublicIp(self, token :str, subscription_id :str, resource_group_name :str, ip_name :str) -> list:
        url = f'https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Network/publicIPAddresses/{ip_name}?api-version=2018-11-01'
        res = requests.get(url, headers={'Authorization': f'Bearer {token}'})
        content = json.loads(res.text)
        return content['properties']['ipAddress']