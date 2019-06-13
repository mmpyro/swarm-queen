#!/bin/bash
rg=$1
numberOfMasters=$2
numberOfWorkers=$3
subscription=$4
clientId=$5
password=$6
tenantId=$7
output='inventory'
retries=0
i=0

if [[ $# -ne 7 ]]
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


while [[ `echo $workerPorts|wc -w` -ne $numberOfWorkers ]] && [[ $retries -lt 3 ]]
do
    echo "retry"
    sleep 10s
    retries=$((retries+1))
    workerPorts=`az network lb inbound-nat-rule list -g ${rg} --lb-name 'worker_lb' -o tsv --query "[].frontendPort"`
done

if [[ "$numberOfMasters" -gt 1 ]]
then
	masterPorts=`az network lb inbound-nat-rule list -g ${rg} --lb-name 'master_lb' -o tsv --query "[].frontendPort"`
else
	masterPorts=22
fi

echo  "[workers]" >> ${output}
for port in ${workerPorts}
do
    echo "worker$i ansible_host=${workerIp} ansible_port=${port}" >> ${output}
    i=$((i+1))
done

i=0
echo "[masters]" >> ${output}
for port in ${masterPorts}
do
    echo "master$i ansible_host=${masterIp} ansible_port=${port}" >> ${output}
    i=$((i+1))
done