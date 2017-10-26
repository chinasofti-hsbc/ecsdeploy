#!/usr/bin/env python
# encoding: utf-8

# Author: Liu Dan <miraclecome (at) gmail.com>

import json
from yaml import load, dump
try:
	from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
	from yaml import Loader, Dumper

def parser(fname):
	with open(fname) as fd:
		data = load(fd, Loader=Loader)
		print(json.dumps(data, indent=4, ensure_ascii=False))

if __name__ == '__main__':
    parser('config.yml')
