#!/usr/bin/env python
# encoding: utf-8

# Author: Liu Dan <miraclecome (at) gmail.com>

import boto3

class Service(object):
    
    def __init__(self, data):
        self.ecs = boto3.client('ecs')
        self.data = data
        
    def create_service(self):
        strategies = []
        constraints = []
        balancers = []
        for i in self.data['Service']['placementStrategy']:
            strategies.append({'type': i['type'], 'field': i['field']})
    
        for i in self.data['Service']['placementConstraints']:
            if i['type'] == 'distinctInstance':
                constraints.append({'type': i['type']})
            else:
                constraints.append({'type': i['type'],
                        'expression': i['expression']})
    
        for i in self.data['Service']['loadBalancers']:
            balancers.append({
                'targetGroupArn': i['targetGroupArn'],
                #'loadBalancerName': i['loadBalancerName'],
                'containerName': i['containerName'],
                'containerPort': i['containerPort']
            })
    
        response = self.ecs.create_service(
            cluster=self.data['Service']['cluster'],
            serviceName=self.data['Service']['name'],
            taskDefinition=self.data['Service']['taskdef'],
            desiredCount=self.data['Service']['desiredCount'],
            role=self.data['Service']['role'],
            deploymentConfiguration={
                'maximumPercent': self.data['Service']['maximumPercent'],
                'minimumHealthyPercent': self.data['Service']['minimumHealthyPercent'],
            },
            placementStrategy=strategies,
            placementConstraints=constraints,
            loadBalancers=balancers)
        
        print ("create service response:%s" % response)
    
