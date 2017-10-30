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
        self.ec2 = Ec2Manager(ecs['Cluster']['instance'])
        self.schedule = Schedule()
        
    def create(self):
        print "****************create cluster********************"
        self.create_cluster();
        time.sleep(5)
        print "****************create instance********************"
        # create instance
        numberOfInstance = self.ecs['Cluster']['numberOfInstance']
        instance = self.ec2.create_instances(numberOfInstance)
        public_ip = self.ec2.get_ipaddr(instance[0])
        document_out = self.schedule.remote_command(public_ip, self.ec2.get_keypair(), 
                                                    'curl http://169.254.169.254/latest/dynamic/instance-identity/document/')
        print "create instance document:%s" % document_out
        documentFile = open('document.json', 'w')
        documentFile.write(document_out)
        documentFile.close()
        signature = self.schedule.remote_command(public_ip, self.ec2.get_keypair(), 
                                                 'curl http://169.254.169.254/latest/dynamic/instance-identity/signature/')
        print "create instance document signature:%s" % signature
        documentSignature = open('signature.txt', 'w')
        documentSignature.write(signature)
        documentSignature.close()
        
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