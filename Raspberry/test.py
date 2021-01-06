#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 22:13:35 2020

@author: Thomas
"""

import time
import numpy as np


from src.State import State
from quaro.HardwareConfig import HardwareConfig
from src.GaitController import GaitController
from src.TouchdownLocalizer import TouchdownLocalizer
from src.SwingController import SwingController
from src.SupportController import SupportController

st = State()
hc = HardwareConfig()
gc = GaitController(st, hc)
tl = TouchdownLocalizer(st)
swc = SwingController(tl)
spc = SupportController(tl)

np.set_printoptions(precision = 2, suppress=True)

for i in range(20):
    print i
    #ls, lt = gc.get_timing()
    #print(swc.get_position(ls, lt))
    #print(spc.get_position(ls, lt))
    print(gc.get_position())
    time.sleep(0.1)

#st.debug()