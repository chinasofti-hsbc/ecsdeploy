#coding=utf-8
from elasticcontainerservice.cluster import Cluster
import sys
import yaml
import time
from core.taskdef import TaskDef
from core.service import Service
from awsapi.ec2manager import Ec2Manager
from autoscaling.applicationautoscaling import ApplicationAutoScaling

#print "hello"   
f = open(sys.argv[1])  
config = yaml.load(f)
autoScaling = ApplicationAutoScaling(config)
autoScaling.register_scalable_target()
autoScaling.put_scaling_policy()
#task = TaskDef(config)
#task.run_task()
#task = Service(config)
#task.create_service()
#ec2 = Ec2Manager(config['Cluster']['instance'])
#ec2.create_instances(1)
#taskdef(config)
#cluster = Cluster(config)
#cluster.create_cluster()
#time.sleep(5)
#print "************************************"
#cluster.create()
#cluster.register_container_instance()


# from awsapi.ec2manager import Ec2Manager
# from core.schedule import Schedule
# config = {
#         'us-east-2': {
#             'keypair': 'jameson-keypair',
#             'amiid': 'ami-c5062ba0',
#             'instancetype': 't2.micro',
#             'securitygroupid': ['sg-5a391333']
#         }
#     }
# ec2 = Ec2Manager(config) 
# # instance = ec2.create_instances(1)
# # print instance
# # print "--------------------"
# # ip = ec2.get_ipaddr(instance[0])
# # print ip
# # print "--------------------"
# ss = Schedule(1, config, 'sdk')
# out = ss.remote_command('18.221.248.108', 'curl http://169.254.169.254/latest/dynamic/instance-identity/document/')
# print out 