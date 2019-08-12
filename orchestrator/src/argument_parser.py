import argparse

def parse():
    arg_parser = argparse.ArgumentParser(description='Setup swarm cluster on Azure cloud.')
    arg_parser.add_argument('--terraform-dir', dest='terraform_directory', required=True,
                            help='directory where terraform scripts are located')
    arg_parser.add_argument('--ansible-dir', dest='ansible_directory', required=True,
                            help='directory where ansible scripts are located')
    arg_parser.add_argument('--config', dest='config', required=True,
                            help='configuration file')
    arg_parser.add_argument('--mode', dest='mode', required=True, default='apply', help='terraform mode: apply|destroy')
    return arg_parser.parse_args()

