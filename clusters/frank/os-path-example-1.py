#!/usr/bin/env python

from __future__ import print_function

import os


filename = "my/little/pony"

print("using", os.name, "...")
print("split", "=>", os.path.split(filename))
print("splitext", "=>", os.path.splitext(filename))
print("dirname", "=>", os.path.dirname(filename))
print("basename", "=>", os.path.basename(filename))
print("join", "=>", os.path.join(os.path.dirname(filename), os.path.basename(filename)))
