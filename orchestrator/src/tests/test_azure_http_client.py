import unittest
import mock
from azure.authorization import AuthorizationDto
from azure.azure_http_client import AzureHttpClient


class AzureHttpClientTests(unittest.TestCase):

    def _mock_response(self, status :int, content :str) -> mock.Mock:
        mock_response = mock.Mock()
        mock_response.status_code = status
        mock_response.content = content
        mock_response.text = content
        return  mock_response

    @mock.patch('requests.post')
    def test_return_authorization_token(self, requests_mock):
        #Given
        mock_response = self._mock_response(200, '{"access_token": "xxx"}')
        requests_mock.return_value = mock_response
        azure_http_client = AzureHttpClient()
        authorization = AuthorizationDto(tenant_id='', client_id='', secret='')

        #When
        token = azure_http_client.getAuthorizationToken(authorization)

        #Then
        self.assertIsNotNone(token)
        self.assertEqual(token, 'xxx')

    @mock.patch('requests.get')
    def test_return_load_balancer_names(self, requests_mock):
        #Given
        mock_response = self._mock_response(200, '{"value": [{"name": "testlb"}] }')
        requests_mock.return_value = mock_response
        azure_http_client = AzureHttpClient()

        #When
        lb_names = azure_http_client.getAzureLoadBalancers(token='', subscription_id='', resource_group_name='')

        #Then
        self.assertIsNotNone(lb_names)
        self.assertEqual(lb_names, ['testlb'])

    @mock.patch('requests.get')
    def test_return_load_balancer_nat_pool(self, requests_mock):
        # Given
        mock_response = self._mock_response(200, '{"properties": { "inboundNatRules": [{"name": "ssh.0","properties": {"frontendPort": 50001} }]} }')
        requests_mock.return_value = mock_response
        azure_http_client = AzureHttpClient()

        # When
        lb_names = azure_http_client.getAzureLoadBalancerNatPool(token='', subscription_id='', resource_group_name='', lb_name='')

        # Then
        self.assertIsNotNone(lb_names)
        self.assertEqual(lb_names, [50001])

    @mock.patch('requests.get')
    def test_return_ip_names(self, requests_mock):
        #Given
        mock_response = self._mock_response(200, '{"value": [{"name": "testip"}] }')
        requests_mock.return_value = mock_response
        azure_http_client = AzureHttpClient()

        #When
        ips = azure_http_client.getAzurePublicIps(token='', subscription_id='', resource_group_name='')

        #Then
        self.assertIsNotNone(ips)
        self.assertEqual(ips, ['testip'])

    @mock.patch('requests.get')
    def test_return_ip_value(self, requests_mock):
        #Given
        mock_response = self._mock_response(200, '{"properties": {"ipAddress": "10.4.1.2" } }')
        requests_mock.return_value = mock_response
        azure_http_client = AzureHttpClient()

        #When
        ip_value = azure_http_client.getAzurePublicIp(token='',subscription_id='', resource_group_name='', ip_name='')

        #Then
        self.assertIsNotNone(ip_value)
        self.assertEqual(ip_value, '10.4.1.2')

if __name__ == '__main__':
    unittest.main()
