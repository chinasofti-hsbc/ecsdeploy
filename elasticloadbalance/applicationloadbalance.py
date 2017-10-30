#coding=utf-8
'''
Created on 2017年10月26日

@author: sean b q xiao
'''
import boto3
import time
import yaml

class ApplicationLoadbaLance(object):
    def __init__(self, elb):
        self.elb = elb
        self.client = boto3.client('elbv2')
    
    def create(self):
        elb = {}
        loadBalance = {}
        loadbalance_response = self.create_load_balancer()
        loadBalancerArn = loadbalance_response['LoadBalancers'][0]['LoadBalancerArn']
        DNSName = loadbalance_response['LoadBalancers'][0]['DNSName']
        time.sleep(5)
        print "************************************"
        target_response = self.create_target_group()
        targetGroupArn = target_response['TargetGroups'][0]['TargetGroupArn']
        targetArn = {'targetGroupArn': targetGroupArn, 'targets': self.elb['ELB']['TargetGroup']['targets']}
        time.sleep(5)
        print "************************************"
        self.register_targets(targetGroupArn);
        time.sleep(5)
        print "************************************"
        listener_response = self.create_listener(loadBalancerArn, targetGroupArn);
        listenerArn = listener_response['Listeners'][0]['ListenerArn']
        loadArn = {'DNSName': DNSName, 'loadBalancerArn': loadBalancerArn, 'listenerArn': listenerArn}
        loadBalance['LoadBalance'] = loadArn
        loadBalance['TargetGroup'] = targetArn
        elb['ELB'] = loadBalance
        #save elb info
        yamlFile = open('elb-info.yaml', "w")  
        yaml.dump(elb, yamlFile)  
        yamlFile.close()
        
        
    def delete(self):
        self.deregister_targets()
        time.sleep(5)
        print "************************************"
        self.delete_listener()
        time.sleep(5)
        print "************************************"
        self.delete_target_group()
        time.sleep(5)
        print "************************************"
        self.delete_load_balancer()
        
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
        
        return response
        
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
        
    def delete_load_balancer(self):
        response = self.client.delete_load_balancer(
            LoadBalancerArn = self.elb['ELB']['LoadBalance']['loadBalancerArn']
        )
        print "delete load balance response:%s" % response
        
    def delete_listener(self):
        response = self.client.delete_listener(
            ListenerArn = self.elb['ELB']['LoadBalance']['listenerArn']
        )
        print "delete listener response:%s" % response
        
    def deregister_targets(self):
        response = self.client.deregister_targets(
            TargetGroupArn = self.elb['ELB']['TargetGroup']['targetGroupArn'],
            Targets = self.elb['ELB']['TargetGroup']['targets']
        )
        print "deregiste target group response:%s" % response
        
    def delete_target_group(self):
        response = self.client.delete_target_group(
            TargetGroupArn = self.elb['ELB']['TargetGroup']['targetGroupArn']
        )
        print "delete target group response:%s" % response