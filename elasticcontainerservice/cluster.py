#coding=utf-8
'''
Created on 2017年10月26日

@author: sean b q xiao
'''
import boto3
import time

class Cluster(object):
    
    def __init__(self, ecs): 
        self.ecs = ecs
        self.client = boto3.client('ecs')
    def create(self):
        self.create_cluster();
        time.sleep(5)
        numberOfInstance = self.ecs['Cluster']['numberOfInstance']
        for i in range(numberOfInstance):
            print "****************register instance %d********************" % (i + 1)
            self.register_container_instance()
            time.sleep(5)
        
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