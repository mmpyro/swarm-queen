class AzureConfig(object):
    def __init__(self, config :dict) -> None:
        super().__init__()
        azure = config['azure']
        self.__resource_group_name = azure['resourceGroup']
        self.__sub_id = azure['subscriptionId']
        self.__tenant = azure['tenantId']
        self.__clientId = azure['clientId']
        self.__secret = azure['clientSecret']

    @property
    def resource_group(self):
        return self.__resource_group_name

    @property
    def subscription_id(self):
        return self.__sub_id

    @property
    def tenant_id(self):
        return self.__tenant

    @property
    def client_id(self):
        return self.__clientId

    @property
    def client_secret(self):
        return self.__secret