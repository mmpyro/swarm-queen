import json
from jinja2 import Template
import argparse
from process_manager import ProcessManager
from enums.terraform_mode import TerraformMode
import os

cwd = os.getcwd()
config = None
rendered_template = None
terraform_directory = None

parser = argparse.ArgumentParser(description='Setup swarm cluster on Azure cloud.')
parser.add_argument('--dir', dest='terraform_directory', required=True, help='directory where terraform scripts are located')
parser.add_argument('--mode', dest='mode', required=True, default='apply', help='terraform mode: apply|destroy')
args = parser.parse_args()
terraform_directory = args.terraform_directory
mode = TerraformMode.APPLY.value if args.mode == 'apply' else TerraformMode.DESTROY.value

with open('config.json', 'r') as file:
    config = json.load(file)
    config['swarm']['sshKeyPath'] = config['swarm']['sshKeyPath'].replace("\\", "\\\\")

with open('parameters.j2', 'r') as file:
    template = Template(file.read())
    rendered_template = template.render(config)

with open(f'{terraform_directory}\parameters.tfvars', 'w') as file:
    file.write(rendered_template)

statusCode = ProcessManager('terraform').with_cwd(args.terraform_directory)\
    .with_args(mode).with_args('-var-file="parameters.tfvars"').with_args('-auto-approve')\
    .start(lambda data: print(data)).wait()
print(f'Terraform status code {statusCode}')


statusCode = ProcessManager('bash')\
    .with_cwd(cwd)\
    .with_args('./output.sh', config['azure']['resourceGroup'])\
    .with_args(config['swarm']['numberOfMasters'])\
    .with_args(config['azure']['subscriptionId'])\
    .with_args(config['azure']['clientId'])\
    .with_args(config['azure']['clientSecret'])\
    .with_args(config['azure']['tenantId'])\
    .start(lambda data: print(data)).wait()
print(f'az status code {statusCode}')

with open('output.json', 'r') as file:
    output = json.load(file)
    print(output)