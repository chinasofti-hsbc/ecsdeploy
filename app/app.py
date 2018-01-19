#!/usr/bin/env python
# encoding: utf-8

# Author: Liu Dan <miraclecome (at) gmail.com>

import json
import sys
sys.path.append('..')

from core.parser import parser
from core.taskdef import TaskDef
from core.service import Service

from elasticloadbalance.applicationloadbalance import ApplicationLoadbaLance
from autoscaling.applicationautoscaling import ApplicationAutoScaling

def load_data(strategy='create'):
    jdata = parser('../conf/{}_service.yml'.format(strategy))
    jdata['Cluster'] = {}

    if 'ELB' not in jdata: jdata['ELB'] = {}

    jdata['ELB']['LoadBalance'] = {}
    with open('../conf/output.json') as fd:
        js = json.load(fd)
        for item in js[u'Stacks'][0][u'Outputs']:
            if item[u'OutputKey'] == u'ECS':
                jdata['Cluster']['name'] = item[u'OutputValue']
            elif item[u'OutputKey'] == u'LoadBalancerUrl':
                jdata['ELB']['LoadBalance']['DNSName'] = item[u'OutputValue']
            elif item[u'OutputKey'] == u'LoadBalancer':
                jdata['ELB']['LoadBalance']['loadBalancerArn'] = item[u'OutputValue']
            elif item[u'OutputKey'] == u'VPCID':
                if 'TargetGroup' in jdata['ELB']:
                    jdata['ELB']['TargetGroup'][0]['vpcId'] = item[u'OutputValue']

    return jdata


def create_service():
    jdata = load_data()

#   Everytime call create_taskdef, create a new revision
#   of task
    task = TaskDef(jdata)
#    task.create_taskdef()

#   target_group and bound listener only do once in reentrant scene
    elb = ApplicationLoadbaLance(jdata)
    alb = elb.create_target_group_under_loadbalance()

#   can not reentrant
    service = Service(jdata)
    service.create_service(alb)

    autoScaling = ApplicationAutoScaling(jdata)
    autoScaling.register_scalable_target()
    autoScaling.put_scaling_policy()


def update_service():
    jdata = load_data(strategy='update')

#   target_group and bound listener only do once in reentrant scene
    if 'TargetGroup' in jdata['ELB']:
        elb = ApplicationLoadbaLance(jdata)
        alb = elb.create_target_group_under_loadbalance()

    service = Service(jdata)
    service.update_service()

#    autoScaling = ApplicationAutoScaling(jdata)
#    autoScaling.register_scalable_target()
#    autoScaling.put_scaling_policy()

if __name__ == '__main__':
#    create_service()
    update_service()
