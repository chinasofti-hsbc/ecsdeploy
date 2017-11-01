#!/usr/bin/env python
# encoding: utf-8

# Author: Liu Dan <miraclecome (at) gmail.com>

from __future__ import division, print_function

import sys
import boto3

class TaskDef(object):
    def __init__(self, data):
        self.client = boto3.client('ecs')
        self.data = data
        
    def create_taskdef(self):
        containers = []
        for container in self.data['TaskDef']['container']:
            containerdef = {}
    
            if 'hardMemory' in container:
                containerdef['memory'] = container['hardMemory']
            if 'softMemory' in container:
                containerdef['memoryReservation'] = container['softMemory']
    
            containerdef['portMappings'] = []
            for i in container['portMappings']:
                host_port, container_port = i.split(':')
                containerdef['portMappings'].append({
                    'hostPort': int(host_port),
                    'containerPort': int(container_port)
                })
    
            containerdef.update({
                'name': container['name'],
                'image': container['image']
            })
            containers.append(containerdef)
    
        response = self.client.register_task_definition(
                family=self.data['TaskDef']['name'],
                taskRoleArn=self.data['TaskDef']['taskRole'],
                containerDefinitions=containers
                )
        print ("create taskdef response:%s" % response)

    def list_taskdef(self):
        """ taskDefinitionArns response:
            [u'arn:aws:ecs:us-east-2:066703160259:task-definition/flasktest8082:2',
             u'arn:aws:ecs:us-east-2:066703160259:task-definition/flasktest8082:3'
            ]
        """
        response = self.client.list_task_definitions(status='ACTIVE')
        names = set([i.split('/')[1].split(':')[0] for i in response[u'taskDefinitionArns']])
        return names
    
    def check_taskdef(self):
        names = self.list_taskdef()
    
        for task in self.data['TaskDef']:
            if task['name'] in names:
                print('Task {} already in Task Definitions, '
                      'Please change a task name.\nSystem Exit'.format(task['name']))
                sys.exit(1)
                
    def run_task(self):
        response = self.client.run_task(
            cluster = self.data['Service']['cluster'],
            taskDefinition = self.data['Service']['taskdef'],
        )
        print ("run taskdef response:%s" % response)

