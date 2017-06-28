#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('services.ice --all -I .')
import drobots
import Services

class RobotControllerDetector(drobots.DetectorController):
    def alert(self, pos, enemies):
        print("Pos:" +str(pos)+" num: "+str(enemies))