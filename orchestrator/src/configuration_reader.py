import json
from abc import ABC, abstractclassmethod
from jsonschema import validate


class ConfigValidator(ABC):

    @abstractclassmethod
    def validate(self):
        pass


class JsonConfigReader(object):

    def __init__(self, validators :list) -> None:
        super().__init__()
        self.__validators = validators

    def read(self, file_name: str):
        with open(file_name, 'r') as file:
            config = json.load(file)
            config['swarm']['sshKeyPath'] = config['swarm']['sshKeyPath'].replace("\\", "\\\\")
            for validator in self.__validators:
                validator.validate(config)
            return config


class JsonConfigValidator(ConfigValidator):

    def __init__(self) -> None:
        super().__init__()
        self.__schema = {
          "$schema": "http://json-schema.org/draft-04/schema#",
          "type": "object",
          "properties": {
            "azure": {
              "type": "object",
              "properties": {
                "subscriptionId": {
                  "type": "string"
                },
                "clientId": {
                  "type": "string"
                },
                "clientSecret": {
                  "type": "string"
                },
                "tenantId": {
                  "type": "string"
                },
                "resourceGroup": {
                  "type": "string"
                },
                "location": {
                  "type": "string"
                },
                "sshAllowedIpAddress": {
                  "type": "string"
                }
              },
              "required": [
                "subscriptionId",
                "clientId",
                "clientSecret",
                "tenantId",
                "resourceGroup",
                "location",
                "sshAllowedIpAddress"
              ]
            },
            "swarm": {
              "type": "object",
              "properties": {
                "numberOfMasters": {
                  "type": "integer"
                },
                "numberOfWorkers": {
                  "type": "integer"
                },
                "masterVmSize": {
                  "type": "string"
                },
                "workerVmSize": {
                  "type": "string"
                },
                "vmUserName": {
                  "type": "string"
                },
                "sshKeyName": {
                  "type": "string"
                },
                "sshPrivateKeyName": {
                  "type": "string"
                },
                "sshKeyPath": {
                  "type": "string"
                },
                "dockerApiPort": {
                  "type": "integer"
                }
              },
              "required": [
                "numberOfMasters",
                "numberOfWorkers",
                "masterVmSize",
                "workerVmSize",
                "vmUserName",
                "sshKeyName",
                "sshPrivateKeyName",
                "sshKeyPath",
                "dockerApiPort"
              ]
            }
          },
          "required": [
            "azure",
            "swarm"
          ]
        }

    def validate(self, json_to_validate):
        validate(instance=json_to_validate, schema=self.__schema)

