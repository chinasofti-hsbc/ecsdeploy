#!/usr/bin/env python
# encoding: utf-8

# Author: Liu Dan <miraclecome (at) gmail.com>

import sys
import os
sys.path.append( os.getcwd() )

from awsapi.ec2manager import Ec2Manager
from core.schedule import Schedule

if __name__ == '__main__':
    config = {
        'Cluster': {
            'name': 'bigdata',
            'numberOfInstance': 3,
            'instance': {
                'amiid': 'ami-00654a65',
                'keypair': 'jameson-keypair.pem',
                'instancetype': 't2.small',
                'securitygroupid': ['sg-817f32e9']
            }
        }
    }
    manager = Ec2Manager(config)
    schedule = Schedule()
