#coding=utf-8
'''
Created on 2017年10月26日

@author: wechat_team_air
'''
import boto3

class ApplicationLoadbaLance(object):
    '''
    classdocs
    '''
    def __init__(self, elb):
        '''
        Constructor
        '''
        self.elb = elb
        self.client = boto3.client('elbv2')
        
    def create(self):
        response = self.client.create_load_balancer(
            Name = self.elb['ELB']['LoadBalance']['name'],
            Subnets = self.elb['ELB']['LoadBalance']['subnetId'],
            SecurityGroups = self.elb['ELB']['LoadBalance']['securityGroup'],
            Scheme = self.elb['ELB']['LoadBalance']['scheme'],
            Type = 'application'
        )
        print response