#!/usr/bin/env python
# encoding: utf-8

# Author: Liu Dan <miraclecome (at) gmail.com>

import sys
import boto3

from parser import parser

client = boto3.client('ecs')

def parse_config(fname):
    return parser(fname)

def taskdef(data):
    for task in data['TaskDef']:
        containers = []
        for container in task['container']:
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

        response = client.register_task_definition(
                family=task['name'],
                taskRoleArn=task['taskRole'],
                containerDefinitions=containers
                )

def list_taskdef(data):
    names = [task['name'] for task in data['TaskDef']]

    response = client.list_task_definitions(status='ACTIVE')
    names = set([i.split('/')[1].split(':')[0] for i in response[u'taskDefinitionArns']])
    return names

def check_taskdef(data):
    names = list_taskdef(data)

    for task in data['TaskDef']:
        if task['name'] in names:
            print('Task {} already in Task Definitions, '
                  'Please change a task name.\nSystem Exit'.format(task['name']))
            sys.exit(1)

if __name__ == '__main__':
    fname = '../test/config.yml'
    data = parse_config(fname)

    check_taskdef(data)
    print('check ok')

