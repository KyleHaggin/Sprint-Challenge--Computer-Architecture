#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

cpu.load(
    'c:/Users/kyleh/Desktop/Repos/Computer-Architecture/ls8/examples/'
    'call.ls8'
    )
cpu.run()
