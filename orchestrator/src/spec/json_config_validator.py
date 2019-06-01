import unittest
import json
from configuration_reader import JsonConfigValidator

class JsonValidatorTests(unittest.TestCase):
    def test_json_validate(self):
        validator = JsonConfigValidator()
        json_to_validate = json.loads('{"azure": {"subscriptionId": "455454"}, "swarm": {}}')
        validator.validate(json_to_validate)


if __name__ == '__main__':
    unittest.main()
