#!/bin/bash
rg=$1
numberOfMasters=$2
subscription=$3
clientId=$4
password=$5
tenantId=$6

if [ $# -ne 6 ]
then
    echo "Insufficient number of parameters"
    exit 1
fi

az login --service-principal --subscription  $subscription -u $clientId  -p $password --tenant $tenantId
if [ $? -ne 0 ]
then
    echo "cannot login to az"
    exit 2
fi
workerIp=`az network public-ip show -g $rg -n 'worker_ip' --query "ipAddress"`
masterIp=`az network public-ip show -g $rg -n 'master_ip' --query "ipAddress"`
workerJson=`az network lb inbound-nat-rule list -g $rg --lb-name 'worker_lb' -o json --query "{ip: 'workerIp', ports:[].frontendPort}"`
if [ "$numberOfMasters" -gt 1 ]
then
	masterJson=`az network lb inbound-nat-rule list -g $rg --lb-name 'master_lb' -o json --query "{ip: 'masterIp', ports:[].frontendPort}"`
else
	masterJson='{"ip": "masterIp", "ports": [22]}'
fi
workerJson=`echo $workerJson|sed s/\"workerIp\"/$workerIp/g`
masterJson=`echo $masterJson|sed s/\'masterIp\'/$masterIp/g`
echo "{\"worker\": $workerJson, \"master\": $masterJson}"|tee output.json