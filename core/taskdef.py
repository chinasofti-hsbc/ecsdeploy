#!/usr/bin/env python
# encoding: utf-8

# Author: Liu Dan <miraclecome (at) gmail.com>

import boto3

from parser import parser

client = boto3.client('ecs')

def taskdef(fname):
    data = parser(fname)

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

        client.register_task_definition(
                family=task['name'],
                taskRoleArn=task['taskRole'],
                containerDefinitions=containers
                )
if __name__ == '__main__':
    taskdef('../test/taskdef_test.yml')
