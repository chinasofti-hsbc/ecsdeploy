#!/usr/bin/env python
# encoding: utf-8

# Author: Liu Dan <miraclecome (at) gmail.com>

import json
from yaml import load
try:
	from yaml import CLoader as Loader
except ImportError:
	from yaml import Loader

def parser(fname):
	with open(fname) as fd:
		data = load(fd, Loader=Loader)
		return data

if __name__ == '__main__':
	data = parser('../test/config.yml')
	print(json.dumps(data, indent=4, ensure_ascii=False))
