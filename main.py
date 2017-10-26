#coding=utf-8
import yaml
import sys
from elasitloadbalance.applicationloadbalance import ApplicationLoadbaLance

def main():
    if len(sys.argv) <= 1:
        print "You must specify a config file."
        exit(-1)
    else:
        f = open(sys.argv[1])  
        config = yaml.load(f)
        
        elb = ApplicationLoadbaLance(config)
        elb.create() 
    

if __name__ == '__main__':
    main()