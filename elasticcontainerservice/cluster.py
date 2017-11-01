#coding=utf-8
'''
Created on 2017年10月26日

@author: sean b q xiao
'''
import boto3
import time
from awsapi.ec2manager import Ec2Manager
from core.schedule import Schedule

class Cluster(object):
    
    def __init__(self, ecs): 
        self.ecs = ecs
        self.client = boto3.client('ecs')
        self.ec2 = Ec2Manager(ecs)
        self.schedule = Schedule()
        
    def create(self):
        print "****************create cluster********************"
        self.create_cluster();
        time.sleep(5)
        print "****************create instance********************"
        # create instance
        instance = self.ec2.create_instances()
        print("create ec2 container:%s" % instance)
        
        return instance
        
    def create_cluster(self):
        response = self.client.create_cluster(
            clusterName = self.ecs['Cluster']['name']
        )
        print "create cluster response:%s" % response
        
        return response
    
    def register_container_instance(self):
        documentFile = open('document.json')
        documentSignature = open('signature.txt')
        ports = []
        for p in self.ecs['Cluster']['resource']['ports']:
            ports.append(str(p))
        response = self.client.register_container_instance(
            cluster = self.ecs['Cluster']['name'],
            instanceIdentityDocument = documentFile.read(),
            instanceIdentityDocumentSignature = documentSignature.read(),
            totalResources=[
                {
                    'name': 'cpu',
                    'type': 'INTEGER',
                    'integerValue': self.ecs['Cluster']['resource']['cpu']
                },
                {
                    'name': 'memory',
                    'type': 'INTEGER',
                    'integerValue': self.ecs['Cluster']['resource']['memory']
                },
                {
                    'name': 'ports',
                    'type': 'STRINGSET',
                    'stringSetValue': ports
                }
            ],
            versionInfo={
                'agentVersion': '1.14.5',
                'dockerVersion': '17.03.2-ce'
            }
        )
        documentFile.close()
        documentSignature.close()
        
        print "register container instance response:%s" % response
        
        return response