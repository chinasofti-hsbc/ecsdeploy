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
        targetGrups = self.elb['ELB']['TargetGroup'];
        targetArns = []
        action = []
        for targetGrup in targetGrups:
            target_response = self.create_target_group(targetGrup)
            targetGroupArn = target_response['TargetGroups'][0]['TargetGroupArn']
            targetArn = {'targetGroupArn': targetGroupArn}
            action.append({'Type': 'forward', 'TargetGroupArn': targetGroupArn})
            time.sleep(5)
#             print "************************************"
#             self.register_targets(targetGroupArn, targetGrup);
#             time.sleep(5)
            print "************************************"
            listener_response = self.create_listener(loadBalancerArn, targetGrup['listener'], targetGroupArn);
            listenerArn = listener_response['Listeners'][0]['ListenerArn']
            targetArn['listenerArn'] = listenerArn
            targetArns.append(targetArn)
        loadArn = {'DNSName': DNSName, 'loadBalancerArn': loadBalancerArn}
        loadBalance['LoadBalance'] = loadArn
        loadBalance['TargetGroup'] = targetArns
        elb['ELB'] = loadBalance
        #save elb info
        yamlFile = open('elb-info.yaml', "w")  
        yaml.dump(elb, yamlFile)  
        yamlFile.close()
        
        return elb
    
    def delete(self):
        targetGrups = self.elb['ELB']['TargetGroup'];
        for targetGrup in targetGrups:
            self.deregister_targets(targetGrup)
            time.sleep(5)
            print "************************************"
            self.delete_listener(targetGrup)
            time.sleep(5)
            print "************************************"
            self.delete_target_group(targetGrup)
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
        
    def create_listener(self, loadBalancerArn, listener, targetArn):
        response = self.client.create_listener(
            LoadBalancerArn = loadBalancerArn,
            Protocol = listener['protocol'],
            Port = listener['port'],
            DefaultActions = [
                {
                    'Type': 'forward',
                    'TargetGroupArn': targetArn
                },
            ]
        )
        print "create loadbalance listener response:%s" % response
        
        return response
        
    def create_target_group(self, targetGrup):
        response = self.client.create_target_group(
            Name = targetGrup['name'],
            Protocol = targetGrup['protocol'],
            Port = targetGrup['port'],
            VpcId = targetGrup['vpcId'],
            HealthCheckProtocol = targetGrup['healthCheckProtocol'],
            HealthCheckPort = targetGrup['healthCheckPort'],
            HealthCheckPath = targetGrup['healthCheckPath'],
            HealthCheckIntervalSeconds = 30,
            HealthCheckTimeoutSeconds = 10,
            HealthyThresholdCount = 5,
            UnhealthyThresholdCount = 3,
            Matcher={
                'HttpCode': '200-299'
            },
            TargetType = targetGrup['targetType']
        )
        print "create target group response:%s" % response
        
        return response
    
    def register_targets(self, targetGroupArn, targetGroup):
        response = self.client.register_targets(
            TargetGroupArn = targetGroupArn,
            Targets = targetGroup['targets']
        )
        print "register target response:%s" % response
        
    def delete_load_balancer(self):
        response = self.client.delete_load_balancer(
            LoadBalancerArn = self.elb['ELB']['LoadBalance']['loadBalancerArn']
        )
        print "delete load balance response:%s" % response
        
    def delete_listener(self, listener):
        response = self.client.delete_listener(
            ListenerArn = listener['listenerArn']
        )
        print "delete listener response:%s" % response
        
    def deregister_targets(self, targetGrup):
        response = self.client.deregister_targets(
            TargetGroupArn = targetGrup['targetGroupArn'],
            Targets = targetGrup['targets']
        )
        print "deregiste target group response:%s" % response
        
    def delete_target_group(self, targetGrup):
        response = self.client.delete_target_group(
            TargetGroupArn = targetGrup['targetGroupArn']
        )
        print "delete target group response:%s" % response