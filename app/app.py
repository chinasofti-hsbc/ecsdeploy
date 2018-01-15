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


def create_service():
    jdata = parser('conf/create_service.yml')
    loadbalance = parser('conf/loadbalance.yml')


    task = TaskDef(jdata)
    task.create_taskdef()

    elb = ApplicationLoadbaLance(jdata)
    alb = elb.create_target_group_under_loadbalance(loadbalance)

    service = Service(jdata)
    service.create_service(alb)

    autoScaling = ApplicationAutoScaling(jdata)
    autoScaling.register_scalable_target()
    autoScaling.put_scaling_policy()


def update_service():
    pass

if __name__ == '__main__':
    create_service()
