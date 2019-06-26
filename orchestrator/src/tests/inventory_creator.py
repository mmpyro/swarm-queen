import unittest
import mock
from inventory.inventory_creator import InventoryCreator
from azure.authorization import AuthorizationDto


class InventoryCreatorTests(unittest.TestCase):

    def _mock_azure_http_client(self):
        azure_client = mock.Mock()
        azure_client.getAuthorizationToken.return_value = ''
        azure_client.getAzurePublicIps.return_value = ['master_ip', 'worker_ip']
        azure_client.getAzurePublicIp.return_value = '10.0.0.0'
        azure_client.getAzureLoadBalancers.return_value = ['worker_lb']
        azure_client.getAzureLoadBalancerNatPool.return_value = [50000, 50001]
        return azure_client


    def test_return_inventory(self):
        #Given
        inventory_creator = InventoryCreator(self._mock_azure_http_client(), '', '')
        expected_inventory = """[primal_master]
master ansible_host=10.0.0.0 ansible_port=22
[workers]
worker1 ansible_host=10.0.0.0 ansible_port=50000
worker2 ansible_host=10.0.0.0 ansible_port=50001
"""

        #When
        inventory = inventory_creator.create(AuthorizationDto('','',''))

        #Then
        self.assertIsNotNone(inventory)
        self.assertEqual(inventory, expected_inventory)

if __name__ == '__main__':
    unittest.main()
