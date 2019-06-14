class AuthorizationDto(object):

    def __init__(self, tenant_id: str, client_id :str, secret :str) -> None:
        super().__init__()
        self.__secret = secret
        self.__client_id = client_id
        self.__tenant_id = tenant_id

    @property
    def secret(self):
        return self.__secret

    @property
    def client_id(self):
        return self.__client_id

    @property
    def tenant_id(self):
        return self.__tenant_id