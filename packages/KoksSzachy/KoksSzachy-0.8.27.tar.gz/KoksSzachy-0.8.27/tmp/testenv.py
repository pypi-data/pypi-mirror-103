#!/usr/bin/env python3

import os
DEBUG = os.getenv("DEBUG", None) is not None

print(DEBUG)

if not DEBUG:
  print('not debug')
