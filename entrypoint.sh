#!/bin/bash

if [[ $# -lt 1 ]]
then
    echo 'mode argument required. apply | destroy'
    exit 1
elif [[ $1 -eq 'apply' ]] || [[ $1 -eq 'destroy' ]]
then
	cd /home/operations/orchestrator/src
    python3 ./main.py --config /home/operations/config.json --terraform-dir /home/operations/terraform --ansible-dir /home/operations/ansible --mode $1
else
    echo 'allowed value for parameter is apply or destroy'
    exit 1
fi