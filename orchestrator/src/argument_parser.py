import argparse

def parse():
    arg_parser = argparse.ArgumentParser(description='Setup swarm cluster on Azure cloud.')
    arg_parser.add_argument('--dir', dest='terraform_directory', required=True,
                            help='directory where terraform scripts are located')
    arg_parser.add_argument('--mode', dest='mode', required=True, default='apply', help='terraform mode: apply|destroy')
    return arg_parser.parse_args()

