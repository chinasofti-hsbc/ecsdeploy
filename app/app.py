#!/usr/bin/env python
# encoding: utf-8

# Author: Liu Dan <miraclecome (at) gmail.com>

import sys
sys.path.append('../')

from core.parser import parser
from core.taskdef import TaskDef
from core.service import Service

from elasticloadbalance.applicationloadbalance import ApplicationLoadbaLance
from autoscaling.applicationautoscaling import ApplicationAutoScaling

def load_data():
    jdata = parser('conf/create_service.yml')
    loadbalance = {'ELB': {}, 'Cluster': {}}
    with open('conf/out.json') as fd:
        js = json.load(fd)
        for item in js[u'Stacks'][0][u'Outputs']:
            if item[u'OutputKey'] == u'ECS':
                loadbalance['Cluster']['name'] = item[u'OutputValue']
            elif item[u'OutputKey'] == u'LoadBalancerUrl':
                loadbalance['ELB']['DNSName'] = item[u'OutputValue']
            elif item[u'OutputKey'] == u'LoadBalancer':
                loadbalance['ELB']['loadBalancerArn'] = item[u'OutputValue']
    return jdata, loadbalance


def create_service():
    jdata, loadbalance = load_data()

    task = TaskDef(jdata)
    task.create_taskdef()

    elb = ApplicationLoadbaLance(jdata)
    alb = elb.create_target_group_under_loadbalance(loadbalance['ELB'])

    service = Service(jdata)
    service.create_service(alb)

    autoScaling = ApplicationAutoScaling(jdata)
    autoScaling.register_scalable_target()
    autoScaling.put_scaling_policy()


def update_service():
    pass

if __name__ == '__main__':
    create_service()
