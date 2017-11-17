#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Yuande Liu <miraclecome (at) gmail.com>

from __future__ import print_function, division

import boto3
import time
from collections import deque


class Ec2Manager(object):

    def __init__(self, config, amiid=None, tag=None):
        self.config = config
        self.tag = tag
        if amiid:
            self.config['Cluster']['instance']['ammid'] = amiid
        self.ec2 = boto3.resource('ec2')
        self.id_instance = {}
        self.id_idx = {}

    def create_instances(self):
        """ ec2.Instance(id='i-336303ac')
        """
        userData = "#!/bin/bash\necho ECS_CLUSTER=" + self.config['Cluster']['name'] + ">> /etc/ecs/ecs.config"
        ins = self.ec2.create_instances(ImageId = self.config['Cluster']['instance']['amiid'],
                                        MinCount = self.config['Cluster']['numberOfInstance'],
                                        MaxCount = self.config['Cluster']['numberOfInstance'],
                                        KeyName = self.config['Cluster']['instance']['keypair'],
                                        InstanceType = self.config['Cluster']['instance']['instancetype'],
                                        SecurityGroupIds = self.config['Cluster']['instance']['securitygroupid'],
                                        IamInstanceProfile={
                                            'Arn': self.config['Cluster']['instance']['iamarn']
                                        },
                                        UserData = userData
                                        )
        print ("create instance response:%s" % ins)
        time.sleep(60)

        for idx, i in enumerate(ins):
            self.id_instance[i.id] = i

        self.queue = deque(ins)
        return self.id_instance.keys()


    def create_instances_v2(self):
        """ ec2.Instance(id='i-336303ac')
        """
        ins = self.ec2.create_instances(ImageId = self.config['Cluster']['instance']['amiid'],
                                        MinCount = self.config['Cluster']['numberOfInstance'],
                                        MaxCount = self.config['Cluster']['numberOfInstance'],
                                        KeyName = self.config['Cluster']['instance']['keypair'],
                                        InstanceType = self.config['Cluster']['instance']['instancetype'],
                                        SecurityGroupIds = self.config['Cluster']['instance']['securitygroupid'])
        time.sleep(60)

        for idx, i in enumerate(ins):
            self.ec2.create_tags(Resources=[i.id],
                    Tags=[{'Key': self.tag, 'Value': self.tag}])
            self.id_instance[i.id] = i
            self.id_idx[i.id] = idx

        self.queue = deque(ins)
        return self.id_instance.keys()
    
    def start(self, ids):
        self.ec2.instances.filter(InstanceIds=ids).start()

    def stop(self, ids):
        self.ec2.instances.filter(InstanceIds=ids).stop()

    def terminate(self, ids):
        self.ec2.instances.filter(InstanceIds=ids).terminate()

    def get_ipaddr(self, one_id):
        i = self.id_instance[one_id]
        i.load()
        return i.public_ip_address

    def get_idx_by_id(self, one_id):
        return self.id_idx[one_id]

    def get_ids_in_status(self, status):
        """
        :param status: pending, running, stopping, stopped, shutting-down
        """
        instances = self.ec2.instances.filter(
                Filters=[{'Name': 'instance-state-name', 'Values': [status]}])
        return [i.id for i in instances]

    def stop_one_and_restart(self):
        instance = self.queue.popleft()

        self.stop([instance.id])
        while 1:
            instance.load() # load cost network time
            if instance.meta.data[u'State'][u'Name'] == 'stopped':
                break

        self.start([instance.id])
        while 1:
            instance.load()
            if instance.meta.data[u'State'][u'Name'] == 'running':
                break

        self.queue.append(instance)
        return instance.id


    def stop_and_start(self, group_num):
        group_instances, ids = [], []
        for _ in xrange(group_num):
            item = self.queue.popleft()
            group_instances.append(item)
            ids.append(item.id)

        self.stop(ids)
        count = [0] * len(ids)
        time.sleep(20)

        start = time.time()
        while 1:
            for idx, val in enumerate(count):
                if val == 0:
                    i = group_instances[idx]
                    if i.meta.data[u'State'][u'Name'] == 'stopped':
                        count[idx] = 1
            if sum(count) == len(ids):
                break
            time.sleep(1)
            [group_instances[idx].load() for idx, val in enumerate(count) if val == 0]
        print('stop {} need: {}'.format(group_num, time.time() - start)) # 20.59s / 9

        self.start(ids)
        count = [0] * len(ids)
        time.sleep(20)

        start = time.time()
        while 1:
            for idx, val in enumerate(count):
                if val == 0:
                    i = group_instances[idx]
                    if i.meta.data[u'State'][u'Name'] == 'running':
                        count[idx] = 1
            if sum(count) == len(ids):
                break
            time.sleep(1)
            [group_instances[idx].load() for idx, val in enumerate(count) if val == 0]
        print('start {} need: {}'.format(group_num, time.time() - start)) # 20.59s / 9

        self.queue.extend(group_instances)
        return ids

if __name__ == '__main__':
    pass
