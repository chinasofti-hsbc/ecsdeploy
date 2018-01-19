#coding=utf-8
'''
@author: Sean
'''
import boto3

class ApplicationAutoScaling(object):
    
    def __init__(self, config):
        self.config = config
        self.client = boto3.client('application-autoscaling')
    
    def register_scalable_target(self, cluster_name=''):
        if 'Cluster' not in self.config:
            resourceId = 'service/' + cluster_name + '/' + self.config['Service']['name']
        else:
            resourceId = 'service/' + self.config['Cluster']['name'] + '/' + self.config['Service']['name']
        response = self.client.register_scalable_target(
            MaxCapacity = int(self.config['AutoScaling']['maxCount']),
            MinCapacity = int(self.config['AutoScaling']['minCount']),
            ResourceId = resourceId,
            RoleARN = self.config['AutoScaling']['iamarn'],
            ScalableDimension = 'ecs:service:DesiredCount',
            ServiceNamespace = 'ecs',
        )
        
        print ("register scaling target response:%s" % response)
        
    def put_scaling_policy(self, cluster_name=''):
        if 'Cluster' not in self.config:
            resourceId = 'service/' + cluster_name + '/' + self.config['Service']['name']
        else:
            resourceId = 'service/' + self.config['Cluster']['name'] + '/' + self.config['Service']['name']
        response = self.client.put_scaling_policy(
            PolicyName = self.config['AutoScaling']['name'],
            PolicyType = 'StepScaling',
            ResourceId = resourceId,
            ScalableDimension = 'ecs:service:DesiredCount',
            ServiceNamespace = 'ecs',
            StepScalingPolicyConfiguration={
                'AdjustmentType': 'PercentChangeInCapacity',
                'Cooldown': 60,
                'StepAdjustments': [
                    {
                        'MetricIntervalLowerBound': 0,
                        'ScalingAdjustment': 200,
                    },
                ],
            },
        )
        
        print("put scaling response:%s" % response)
