#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('services.ice --all -I .')
import drobots
import math
import random
import Container
import Services


class RobotControllerAtaque(Services.AttackerController):
    def __init__(self, bot, key, current=None):
        self.bot = bot
        self.key = key
        self.container = None
        self.listAttaker = []
        self.listDefender = []
        self.listCompleto = []
        self.firstTime = True

    def setLists(self):
        controllers = self.container.listController()
        for key in controllers.keys():
            if key != self.key and key[:3] == self.key[:3]:
                if key[-1] == "D":
                    self.listDefender.append(controllers[key])
                elif key[-1] == "A":
                    self.listAttaker.append(controllers[key])
                elif key[-1] == "C":
                    self.listCompleto.append(controllers[key])


    def turn(self, current=None):
        print("ATACANTE: Entrando turn")
        sys.stdout.flush()
        if self.firstTime:
            self.setLists()
        self.firstTime = False

    def setContainer(self, proxy):
        self.container = Services.ContainerPrx.checkedCast(proxy)

    def robotDestroyed(self, current=None):
        print("Robot atacante destruido")
        sys.stdout.flush()

class RobotControllerDefensa(Services.DefenderController):
    def __init__(self, bot, key, current=None):
        self.bot = bot
        self.key = key
        self.container = None
        self.listAttaker = []
        self.listDefender = []
        self.listCompleto = []
        self.firstTime = True

    def setLists(self):
        controllers = self.container.listController()
        for key in controllers.keys():
            if key != self.key and key[:3] == self.key[:3]:
                if key[-1] == "D":
                    self.listDefender.append(controllers[key])
                elif key[-1] == "A":
                    self.listAttaker.append(controllers[key])
                elif key[-1] == "C":
                    self.listCompleto.append(controllers[key])

    def turn(self, current=None):
        print("DEFENSOR: Entrando turn")
        sys.stdout.flush()
        if self.firstTime:
            self.setLists()
        self.firstTime = False

    def setContainer(self, proxy):
        self.container = Services.ContainerPrx.checkedCast(proxy)

    def robotDestroyed(self, current=None):
        print("Robot defensor destruido")
        sys.stdout.flush()

class RobotController(drobots.RobotController):
    def __init__(self, bot, key, current=None):
        self.bot = bot
        self.key = key
        self.container = None
        self.listAttaker = []
        self.listDefender = []
        self.listCompleto = []
        self.firstTime = True

    def setLists(self):
        controllers = self.container.listController()
        for key in controllers.keys():
            if key != self.key and key[:3] == self.key[:3]:
                if key[-1] == "D":
                    self.listDefender.append(controllers[key])
                elif key[-1] == "A":
                    self.listAttaker.append(controllers[key])
                elif key[-1] == "C":
                    self.listCompleto.append(controllers[key])

    def turn(self, current=None):
        print("COMPLETO: Entrando turn")
        sys.stdout.flush()
        if self.firstTime:
            self.setLists()
        self.firstTime = False

    def setContainer(self, proxy):
        self.container = Services.ContainerPrx.checkedCast(proxy)

    def robotDestroyed(self, current=None):
        print("Robot atacante destruido")
        sys.stdout.flush()