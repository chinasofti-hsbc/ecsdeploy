#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Yuande Liu <miraclecome (at) gmail.com>

from __future__ import print_function, division

import time
import paramiko
from paramiko.ssh_exception import NoValidConnectionsError

class Schedule(object):

    def __init__(self, *args, **kwargs):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        paramiko.util.log_to_file('aws_ssh_login.log')
         
    def remote_command(self, ipaddr, key_file, command, repeat=20):
        out = ''
        for _ in range(repeat):
            try:
                self.ssh.connect(hostname = ipaddr,
                            port = 22,
                            username = 'ec2-user',
                            pkey = paramiko.RSAKey.from_private_key_file(key_file))
                ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command(command)
                out = ssh_stdout.read().decode()
                break
            except NoValidConnectionsError:
                time.sleep(10)
            except:
                time.sleep(10)
        self.ssh.close()
        
        return out

