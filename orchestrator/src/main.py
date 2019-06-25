from argument_parser import parse
from azure.authorization import AuthorizationDto
from azure.azure_http_client import AzureHttpClient
from inventory.inventory_creator import InventoryCreator
from enums.terraform_mode import TerraformMode
from configuration_reader import JsonConfigReader, JsonConfigValidator
from inventory.inventory_writer import InventoryWriter
from process_manager import ProcessManager
from template_processor import TemplateProcessor
import os

cwd = os.getcwd()
config = JsonConfigReader([JsonConfigValidator()]).read(file_name='utils/config.json')
args = parse()
terraform_directory = args.terraform_directory
mode = TerraformMode.APPLY.value if args.mode == 'apply' else TerraformMode.DESTROY.value

output_parameters_path = os.path.join(terraform_directory, 'parameters.tfvars')
template_processor = TemplateProcessor('utils/parameters.j2', output_parameters_path)
template_processor.process(config)

statusCode = ProcessManager('terraform').with_cwd(args.terraform_directory)\
    .with_args(mode, '-var-file="parameters.tfvars"', '-auto-approve')\
    .start(lambda data: print(data)).wait()
print(f'Terraform status code {statusCode}')

if statusCode == 0 and mode == TerraformMode.APPLY.value:
    subscription_id = config['azure']['subscriptionId']
    resource_group = config['azure']['resourceGroup']
    tenant_id = config['azure']['tenantId']
    client_id = config['azure']['clientId']
    client_secret = config['azure']['clientSecret']

    inventory_creator = InventoryCreator(AzureHttpClient(), subscription_id, resource_group)
    inventory = inventory_creator.create(AuthorizationDto(tenant_id, client_id, client_secret))
    inventory_writer = InventoryWriter('swarm_inventory')
    inventory_writer.save(inventory)


