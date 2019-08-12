import os
from argument_parser import parse
from azure.authorization import AuthorizationDto
from azure.azure_http_client import AzureHttpClient
from configuration import Configuration
from configuration_reader import JsonConfigReader, JsonConfigValidator
from enums.terraform_mode import TerraformMode
from inventory.inventory_creator import InventoryCreator
from inventory.inventory_writer import InventoryWriter
from process_manager import ProcessManager
from template_processor import TemplateProcessor

cwd = os.getcwd()
args = parse()
config = JsonConfigReader([JsonConfigValidator()]).read(file_name=args.config)
terraform_directory = args.terraform_directory
ansible_directory = args.ansible_directory
mode = TerraformMode.APPLY.value if args.mode == 'apply' else TerraformMode.DESTROY.value

output_parameters_path = os.path.join(terraform_directory, 'parameters.tfvars')
template_processor = TemplateProcessor('utils/parameters.j2', output_parameters_path)
template_processor.process(config)

status_code = ProcessManager('terraform').with_cwd(args.terraform_directory)\
    .with_args(mode, '-var-file="parameters.tfvars"', '-auto-approve')\
    .start(lambda data: print(data)).wait()
print(f'Terraform status code {status_code}')

if status_code == 0 and mode == TerraformMode.APPLY.value:
    configuration = Configuration(config)
    tenant_id = configuration.azure.tenant_id
    client_id = configuration.azure.client_id
    client_secret = configuration.azure.client_secret

    inventory_creator = InventoryCreator(AzureHttpClient(), configuration)
    inventory = inventory_creator.create(AuthorizationDto(tenant_id, client_id, client_secret))
    inventory_writer = InventoryWriter('swarm_inventory')
    inventory_writer.save(inventory)
    print('Inventory created')
    print('Start Ansible')
    status_code = ProcessManager('ansible-playbook').with_cwd(ansible_directory)\
    .with_args('-i',f'{cwd}/swarm_inventory', 'swarm.yaml', '-u',
               configuration.swarm.user_name,'-b',f'--key-file={configuration.swarm.ssh_private_key_full_name}')\
    .with_env(ANSIBLE_HOST_KEY_CHECKING='False')\
    .start(lambda data: print(data)).wait()
    print(f'Ansible has finished with {status_code} code.')


