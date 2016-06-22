# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('drobots.ice')
import drobots
Ice.loadSlice('-I %s services.ice' % Ice.getSliceDir())
import Services
import math
import random
import Container

class RobotControllerAtaque(drobots.RobotControllerAtaque):
    def __init__(self,bot,container):
        self.bot = bot
        self.speed = 100
        self.i = 0
        self.container = container
        self.anguloDisparo = None
        self.proxys = None

    def getTipo(self):
        return "ataque"

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
        nProxys = len(self.proxys)
        random.randint(1, 100)

        n = random.randint(1,nProxys)

        print(self.proxys[n].getAnguloDisparo())


    def turn(self,current=None):
        if( self.proxys is None):
            self.proxys = self.getProxys()
        location = self.bot.location()
        angulo = math.atan(location.y/location.x)
        if(self.i%2==0):
            self.bot.cannon(angulo, self.speed)
            self.disparar()
        else:
            self.mover(location, angulo)

        self.i = self.i+1

    def getProxys(self):
        proxys = []
        lista = self.container.list()

        for i in range(1, len(lista)+1):
            proxy = lista[str(i)]
            proxy = drobots.RobotControllerPrx.uncheckedCast(proxy)
            proxys.append(proxy)
            print("1")
        return proxys

        # if(location.x == 500):container.list()
        #     if location.y > 500:
        #         if(self.bot.scan(angulo,self.speed)):
        #             self.bot.cannon(270,self.speed)
        #         else:
        #             self.bot.drive(270,self.speed)
        #     else:
        #         if(self.bot.scan(90,self.speed)):
        #             self.bot.cannon(90,self.speed)
        #         else:
        #             self.bot.drive(90,self.speed)
        # elif location.y == 500:
        #     if location.x > 500:
        #         if(self.bot.scan(180,self.speed)):
        #             self.bot.cannon(180,self.speed)
        #         else:
        #             self.bot.drive(180,self.speed)
        #     else:
        #         if(self.bot.scan(0,self.speed)):
        #             self.bot.cannon(0,self.speed)
        #         else:
        #             self.bot.drive(0,self.speed)
        # elif(location.y <500 and location.x <500):
        #     if(self.bot.scan(angulo,self.speed)):
        #         self.bot.cannon(angulo,self.speed)
        #     else:
        #         self.bot.drive(angulo,self.speed)
        # elif(location.y >500 and location.x >500):
        #     if(self.bot.scan(180+angulo,self.speed)):
        #         self.bot.cannon(180+angulo,self.speed)
        #     else:
        #         self.bot.drive(180+angulo,self.speed)
        # elif(location.y >500 and location.x <500):
        #     if(self.bot.scan(270+angulo,self.speed)):
        #         self.bot.cannon(270+angulo,self.speed)
        #     else:
        #         self.bot.drive(270+angulo,self.speed)
        # elif(location.y <500 and location.x > 500):
        #     if(self.bot.scan(90+angulo,self.speed)):
        #         self.bot.cannon(90+angulo,self.speed)
        #     else:
        #         self.bot.drive(90+angulo,self.speed)
        #
        # if(location.x  > 490 and location.x < 510 and location.y  > 480 and location.y < 510):
        #     self.speed = 10
        #     if location.x == 500 and location.y == 500:
        #         self.bot.drive(angulo,40)
        # else:
        #     self.speed = 100


    def robotDestroyed(self, current=None):
        print("Robot atacante destruido")

class RobotControllerDefensa(drobots.RobotControllerDefensa):
    def __init__(self, bot, container):
        self.bot = bot
        self.speed = 100
        self.i = 0
        self.danyo = 0
        self.container = container
        self.anguloDisparo = None
        self.proxys = container.list()

    def getTipo(self):
        return "defensa"

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

        if (self.bot.damage() > self.danyo):
            self.mover(location,angulo)
        else:
            self.bot.drive(angulo, 0)
            self.scan()

    def getAnguloDisparo(self):
        return self.anguloDisparo



    def robotDestroyed(self, current=None):
        print("Robot defensor destruido")
