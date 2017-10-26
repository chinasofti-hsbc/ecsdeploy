#!/usr/bin/env python
# encoding: utf-8

# Author: Liu Dan <miraclecome (at) gmail.com>

from yaml import load, dump
try:
	from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
	from yaml import Loader, Dumper

def parser(fname):
	with open(fname) as fd:
		data = load(fd, Loader=Loader)
		print(data)

if __name__ == '__main__':
    parser('config.yml')
