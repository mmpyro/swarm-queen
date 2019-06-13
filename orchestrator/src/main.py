from argument_parser import parse
from process_manager import ProcessManager
from enums.terraform_mode import TerraformMode
from configuration_reader import JsonConfigReader, JsonConfigValidator
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

if mode == TerraformMode.APPLY.value and statusCode == 0:
    statusCode = ProcessManager('bash')\
        .with_cwd(cwd)\
        .with_args('./utils/output.sh')\
        .with_args(config['azure']['resourceGroup'], config['swarm']['numberOfMasters'], config['swarm']['numberOfWorkers'])\
        .with_args(config['azure']['subscriptionId'], config['azure']['clientId'])\
        .with_args(config['azure']['clientSecret'], config['azure']['tenantId'])\
        .start(lambda data: print(data)).wait()
    print(f'az status code {statusCode}')

