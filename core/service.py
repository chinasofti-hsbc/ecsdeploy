#!/usr/bin/env python
# encoding: utf-8

# Author: Liu Dan <miraclecome (at) gmail.com>

import boto3

from parser import parser

client = boto3.client('ecs')

def parse_config(fname):
    return parser(fname)

def service(cluster, service, taskdef, ):
    strategies = []
    constraints = []
    balancers = []
    for i in data['Service']['placementStrategy']:
        strategies.append({'type': i['type'], 'field': i['field']})

    for i in data['Service']['placementConstraints']:
        if i['type'] == 'distinctInstance':
            constraints.append({'type': i['type']})
        else:
            constraints.append({'type': i['type'],
                    'expression': i['expression']})

    for i in data['Service']['loadBalancers']:
        balancers.append({
            'targetGroupArn': i['targetGroupArn'],
            'loadBalancerName': i['loadBalancerName'],
            'containerName': i['containerName'],
            'containerPort': i['containerPort']
        })

    response = create_service()
        cluster=data['Service']['cluster'],
        serviceName=data['Service']['name'],
        taskDefinition=data['Service']['taskdef'],
        desiredCount=data['Service']['desiredCount'],
        role=data['Service']['role'],
        deploymentConfiguration={
            'maximumPercent': data['Service']['maximumPercent'],
            'minimumHealthyPercent': data['Service']['minimumHealthyPercent'],
        },
        placementStrategy=strategies,
        placementConstraints=constraints,
        loadBalancers=balancers)

