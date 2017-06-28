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


class RobotControllerAtaque(drobots.RobotController):
    def __init__(self, bot):
        self.bot = bot
        self.speed = 100
        self.i = 0
        self.container = None
        self.anguloDisparo = None
        #self.bot_id = id

    def mover(self, location, angulo):
        if (location.x == 500):
            if location.y > 500:
                self.bot.drive(270, self.speed)
            else:
                self.bot.drive(90, self.speed)
        elif location.y == 500:
            if location.x > 500:
                self.bot.drive(180, self.speed)
            else:
                self.bot.drive(0, self.speed)
        elif (location.y < 500 and location.x < 500):
            self.bot.drive(angulo, self.speed)
        elif (location.y > 500 and location.x > 500):
            self.bot.drive(180 + angulo, self.speed)
        elif (location.y > 500 and location.x < 500):
            self.bot.drive(270 + angulo, self.speed)
        elif (location.y < 500 and location.x > 500):
            self.bot.drive(90 + angulo, self.speed)

        if (location.x > 490 and location.x < 510 and location.y > 480 and location.y < 510):
            self.speed = 10
            if location.x == 500 and location.y == 500:
                self.bot.drive(angulo, 40)
        else:
            self.speed = 100

    def disparar(self):
        print (self.bot.damage())
        #nProxys = len(self.proxys)
        random.randint(1, 100)

        #n = random.randint(1,nProxys)

        #print(self.proxys[n].getAnguloDisparo())



    def turn(self,current=None):
        print (self.bot.damage())
        #if( self.proxys is None):
        #    self.proxys = self.getProxys()
        location = self.bot.location()
        angulo = math.atan(location.y/location.x)
        if(self.i%2==0):
            self.bot.cannon(angulo, self.speed)
            self.disparar()
        else:
            self.mover(location, angulo)

        self.i += 1

    def getProxys(self, current=None):
        proxys = []

        proxy_container = current.adapter.getCommunicator().stringToProxy("container")
        container = Services.ContainerPrx.checkedCast(proxy_container)
        lista = container.list()

        for i in range(1, len(lista)+1):
            proxy = lista[str(i)]
            proxy = drobots.RobotControllerPrx.uncheckedCast(proxy)
            proxys.append(proxy)
        return proxys

    def robotDestroyed(self, current=None):
        print("Robot atacante destruido")

class RobotControllerDefensa(drobots.RobotController):
    def __init__(self, bot):
        self.speed = 100
        self.i = 0
        self.danyo = 0
        self.anguloDisparo = None
        self.bot = bot

    def mover(self,location,angulo):
        if (location.x == 500):
            if location.y > 500:
                self.bot.drive(270, self.speed)
            else:
                self.bot.drive(90, self.speed)
        elif location.y == 500:
            if location.x > 500:
                self.bot.drive(180, self.speed)
            else:
                self.bot.drive(0, self.speed)
        elif (location.y < 500 and location.x < 500):
            self.bot.drive(angulo, self.speed)
        elif (location.y > 500 and location.x > 500):
            self.bot.drive(180 + angulo, self.speed)
        elif (location.y > 500 and location.x < 500):
            self.bot.drive(270 + angulo, self.speed)
        elif (location.y < 500 and location.x > 500):
            self.bot.drive(90 + angulo, self.speed)

        if (location.x > 490 and location.x < 510 and location.y > 480 and location.y < 510):
            self.speed = 10
            if location.x == 500 and location.y == 500:
                self.bot.drive(angulo, 40)
        else:
            self.speed = 100

    def scan(self):
        angulo = random.randint(0,359)
        detectados = self.bot.scan(angulo, 30)

        if detectados != 0:
            self.bot.drive(0, 0)
            self.anguloDisparo = angulo

        print("Angulo: " + str(angulo) + "Enemigos: " + str(detectados))


    def turn(self, current=None):
        location = self.bot.location()
        angulo = math.atan(location.y / location.x)

        self.i = self.i + 1
        location = self.bot.location()
        print(location)
        self.mover(location, angulo)

        #if (self.bot.damage() > self.danyo):
        #    self.mover(location,angulo)
        #else:
        #    self.bot.drive(angulo, 0)
        #    #self.scan()

    def getAnguloDisparo(self):
        return self.anguloDisparo



    def robotDestroyed(self, current=None):
        print("Robot defensor destruido")

class RobotController(drobots.RobotController):
    def __init__(self, bot):
        self.bot = bot
        self.speed = 100
        self.i = 0
        self.container = None
        self.anguloDisparo = None
        #self.bot_id = id

    def mover(self, location, angulo):
        if (location.x == 500):
            if location.y > 500:
                self.bot.drive(270, self.speed)
            else:
                self.bot.drive(90, self.speed)
        elif location.y == 500:
            if location.x > 500:
                self.bot.drive(180, self.speed)
            else:
                self.bot.drive(0, self.speed)
        elif (location.y < 500 and location.x < 500):
            self.bot.drive(angulo, self.speed)
        elif (location.y > 500 and location.x > 500):
            self.bot.drive(180 + angulo, self.speed)
        elif (location.y > 500 and location.x < 500):
            self.bot.drive(270 + angulo, self.speed)
        elif (location.y < 500 and location.x > 500):
            self.bot.drive(90 + angulo, self.speed)

        if (location.x > 490 and location.x < 510 and location.y > 480 and location.y < 510):
            self.speed = 10
            if location.x == 500 and location.y == 500:
                self.bot.drive(angulo, 40)
        else:
            self.speed = 100

    def scan(self):
        angulo = random.randint(0,359)
        detectados = self.bot.scan(angulo, 30)

        if detectados != 0:
            self.bot.drive(0, 0)
            self.anguloDisparo = angulo

        print("Angulo: " + str(angulo) + "Enemigos: " + str(detectados))

    def disparar(self):
        print (self.bot.damage())
        #nProxys = len(self.proxys)
        random.randint(1, 100)

        #n = random.randint(1,nProxys)

        #print(self.proxys[n].getAnguloDisparo())



    def turn(self,current=None):
        print (self.bot.damage())
        #if( self.proxys is None):
        #    self.proxys = self.getProxys()
        location = self.bot.location()
        angulo = math.atan(location.y/location.x)
        if(self.i%2==0):
            self.bot.cannon(angulo, self.speed)
            self.disparar()
        else:
            self.mover(location, angulo)

        self.i += 1


    def robotDestroyed(self, current=None):
        print("Robot atacante destruido")