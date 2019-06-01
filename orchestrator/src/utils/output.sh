#!/bin/bash
rg=$1
numberOfMasters=$2
subscription=$3
clientId=$4
password=$5
tenantId=$6
output='inventory'

if [[ $# -ne 6 ]]
then
    echo "Insufficient number of parameters"
    exit 1
fi

az login --service-principal --subscription  ${subscription} -u ${clientId}  -p ${password} --tenant ${tenantId}
if [[ $? -ne 0 ]]
then
    echo "cannot login to az"
    exit 2
fi
rm ${output}
workerIp=`az network public-ip show -g ${rg} -n 'worker_ip' --query "ipAddress" -o tsv`
masterIp=`az network public-ip show -g ${rg} -n 'master_ip' --query "ipAddress" -o tsv`
workerPorts=`az network lb inbound-nat-rule list -g ${rg} --lb-name 'worker_lb' -o tsv --query "[].frontendPort"`
if [[ "$numberOfMasters" -gt 1 ]]
then
	masterPorts=`az network lb inbound-nat-rule list -g ${rg} --lb-name 'master_lb' -o tsv --query "[].frontendPort"`
else
	masterPorts=22
fi

echo  "[workers]" >> ${output}
for port in ${workerPorts}
do
    echo "${workerIp} ansible_port=${port}" >> ${output}
done

echo "[masters]" >> ${output}
for port in ${masterPorts}
do
    echo "${masterIp} ansible_port=${port}" >> ${output}
done