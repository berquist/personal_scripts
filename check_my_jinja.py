#!/usr/bin/env python
# https://stackoverflow.com/a/37939821/
import sys
from jinja2 import Environment

env = Environment()
with open(sys.argv[1]) as template:
    env.parse(template.read())
