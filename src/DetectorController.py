#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('services.ice --all -I .')
import drobots
import Services

class RobotControllerDetector(Services.DetectorControllerI):
    def __init__(self, current=None):
        self.posicion = None
        self.enemies = 0

    def alert(self, pos, enemies, current=None):
        print("DETECTOR: Detectados " + str(enemies) + " enemigos")
        sys.stdout.flush()
        self.posicion = pos
        self.enemies = enemies

    def posicion(self, current=None):
        if self.enemies > 0:
            return self.posicion
        else:
            return None

    def getEnemigoX(self, current=None):
        if self.enemies > 0 and self.posicion is not None:
            return self.posicion.x
        else:
            return -1

    def getEnemigoY(self, current=None):
        if self.enemies > 0 and self.posicion is not None:
            return self.posicion.y
        else:
            return -1
