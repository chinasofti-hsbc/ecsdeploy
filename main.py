#coding=utf-8
import yaml
import sys
from elasticloadbalance.applicationloadbalance import ApplicationLoadbaLance
from elasticcontainerservice.cluster import Cluster
from core.taskdef import TaskDef
from core.service import Service
from autoscaling.applicationautoscaling import ApplicationAutoScaling

def main():
    if len(sys.argv) <= 1:
        print "You must specify a config file."
        exit(-1)
    else:
        f = open(sys.argv[1])  
        config = yaml.load(f)
        #crete cluster
        cluster = Cluster(config)
        cluster.create()
        
        #create taskdef
        task = TaskDef(config)
        task.create_taskdef()
        
        #create elb
        elb = ApplicationLoadbaLance(config)
        loadBalance = elb.create() 
        
        #create service
        service = Service(config)
        service.create_service(loadBalance)
        
        #add auto scaling
        autoScaling = ApplicationAutoScaling(config)
        autoScaling.register_scalable_target()
        autoScaling.put_scaling_policy()
    

if __name__ == '__main__':
    main()