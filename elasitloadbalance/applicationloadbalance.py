#coding=utf-8
'''
Created on 2017年10月26日

@author: sean b q xiao
'''
import boto3
import time

class ApplicationLoadbaLance(object):
    def __init__(self, elb):
        self.elb = elb
        self.client = boto3.client('elbv2')
    
    def create(self):
        loadbalance_response = self.create_load_balancer()
        loadBalancerArn = loadbalance_response['LoadBalancers'][0]['LoadBalancerArn']
        time.sleep(5)
        print "************************************"
        target_response = self.create_target_group()
        targetGroupArn = target_response['TargetGroups'][0]['TargetGroupArn']
        time.sleep(5)
        print "************************************"
        self.register_targets(targetGroupArn);
        time.sleep(5)
        print "************************************"
        self.create_listener(loadBalancerArn, targetGroupArn);
        
    def create_load_balancer(self):
        response = self.client.create_load_balancer(
            Name = self.elb['ELB']['LoadBalance']['name'],
            Subnets = self.elb['ELB']['LoadBalance']['subnetId'],
            SecurityGroups = self.elb['ELB']['LoadBalance']['securityGroup'],
            Scheme = self.elb['ELB']['LoadBalance']['scheme'],
            Type = 'application'
        )
        print "create application loadbalance response:%s" % response
        
        return response
        
    def create_listener(self, loadBalancerArn, targetGroupArn):
        response = self.client.create_listener(
            LoadBalancerArn = loadBalancerArn,
            Protocol = self.elb['ELB']['LoadBalance']['listener']['protocol'],
            Port = self.elb['ELB']['LoadBalance']['listener']['port'],
            DefaultActions=[
                {
                    'Type': 'forward',
                    'TargetGroupArn': targetGroupArn
                },
            ]
        )
        print "create loadbalance listener response:%s" % response
        
    def create_target_group(self):
        response = self.client.create_target_group(
            Name = self.elb['ELB']['TargetGroup']['name'],
            Protocol = self.elb['ELB']['TargetGroup']['protocol'],
            Port = self.elb['ELB']['TargetGroup']['port'],
            VpcId = self.elb['ELB']['TargetGroup']['vpcId'],
            HealthCheckProtocol = self.elb['ELB']['TargetGroup']['healthCheckProtocol'],
            HealthCheckPort = self.elb['ELB']['TargetGroup']['healthCheckPort'],
            HealthCheckPath = self.elb['ELB']['TargetGroup']['healthCheckPath'],
            HealthCheckIntervalSeconds = 30,
            HealthCheckTimeoutSeconds = 10,
            HealthyThresholdCount = 5,
            UnhealthyThresholdCount = 3,
            Matcher={
                'HttpCode': '200-299'
            },
            TargetType = self.elb['ELB']['TargetGroup']['targetType']
        )
        print "create target group response:%s" % response
        
        return response
    
    def register_targets(self, targetGroupArn):
        response = self.client.register_targets(
            TargetGroupArn = targetGroupArn,
            Targets = self.elb['ELB']['TargetGroup']['targets']
        )
        print "register target response:%s" % response