#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

cpu.load(
    'c:/Users/kyleh/Desktop/Repos/Sprint-Challenge--Computer-Architecture/'
    # 'examples/call.ls8'
    'sctest.ls8'
    )
cpu.run()
