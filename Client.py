#!/usr/bin/python
# -*- mode:python; coding: utf-8; tab-width -*-

import sys
import Ice
Ice.loadSlice('drobots.ice')
import drobots
import math
import random

class Cliente(Ice.Application):
    def run(self, argv):

        broker = self.communicator()

        adapter = broker.createObjectAdapter('PlayerAdapter')

        playerServant = PlayerI(adapter)
        proxyPlayer = adapter.addWithUUID(playerServant)


        player=drobots.PlayerPrx.checkedCast(proxyPlayer)

        proxyGame = broker.stringToProxy(argv[1])
        game = drobots.GamePrx.checkedCast(proxyGame)

        adapter.activate()
        nick = ''.join(random.choice('qwertyuiopasdfghjkl') for _ in range(3))
        game.login(player,nick)

        self.shutdownOnInterrupt()
        broker.waitForShutdown()

class PlayerI(drobots.Player):

    def __init__(self,adapter):
        self.adapter = adapter #current

    def makeController(self,bot,current=None):
        if (bot.ice_isA("::drobots::Attacker")):
            RobotControllerServant = RobotControllerAtaque(bot)
        elif (bot.ice_isA("::drobots::Defender")):
            RobotControllerServant = RobotControllerDefensa(bot)
        proxyRobotController = current.adapter.addWithUUID(RobotControllerServant)
        return drobots.RobotControllerPrx.uncheckedCast(proxyRobotController)
    def win(self,current=None):
        print("Ganaste")
        current.adapter.getCommunicator().shutdown()
    def lose(self,current=None):
        print("Perdiste")
        current.adapter.getCommunicator().shutdown()

class RobotControllerAtaque(drobots.RobotController):
    def __init__(self,bot):
        self.bot = bot
        self.speed = 100
        self.i = 0
    def turn(self,current=None):
        location = self.bot.location()
        angulo = math.atan(location.y/location.x)
        if(self.i%2==0):
            self.bot.cannon(angulo, self.speed)
        else:
            self.bot.drive(angulo, self.speed)

        self.i = self.i+1

        # if(location.x == 500):
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
        print("El robot ha sido destruido")

class RobotControllerDefensa(drobots.RobotController):
    def __init__(self, bot):
        self.bot = bot
        self.speed = 100
        self.i = 0

    def turn(self, current=None):
        location = self.bot.location()
        angulo = math.atan(location.y / location.x)

        if (self.i % 2 == 0):
            self.bot.scan(angulo, self.speed)
        else:
            self.bot.drive(angulo, self.speed)

        self.i = self.i + 1

        # if (location.x == 500):
        #     if location.y > 500:
        #         if (self.bot.scan(angulo, self.speed)):
        #             self.bot.cannon(270, self.speed)
        #         else:
        #             self.bot.drive(270, self.speed)
        #     else:
        #         if (self.bot.scan(90, self.speed)):
        #             self.bot.cannon(90, self.speed)
        #         else:
        #             self.bot.drive(90, self.speed)
        # elif location.y == 500:
        #     if location.x > 500:
        #         if (self.bot.scan(180, self.speed)):
        #             self.bot.cannon(180, self.speed)
        #         else:
        #             self.bot.drive(180, self.speed)
        #     else:
        #         if (self.bot.scan(0, self.speed)):
        #             self.bot.cannon(0, self.speed)
        #         else:
        #             self.bot.drive(0, self.speed)
        # elif (location.y < 500 and location.x < 500):
        #     if (self.bot.scan(angulo, self.speed)):
        #         self.bot.cannon(angulo, self.speed)
        #     else:
        #         self.bot.drive(angulo, self.speed)
        # elif (location.y > 500 and location.x > 500):
        #     if (self.bot.scan(180 + angulo, self.speed)):
        #         self.bot.cannon(180 + angulo, self.speed)
        #     else:
        #         self.bot.drive(180 + angulo, self.speed)
        # elif (location.y > 500 and location.x < 500):
        #     if (self.bot.scan(270 + angulo, self.speed)):
        #         self.bot.cannon(270 + angulo, self.speed)
        #     else:
        #         self.bot.drive(270 + angulo, self.speed)
        # elif (location.y < 500 and location.x > 500):
        #     if (self.bot.scan(90 + angulo, self.speed)):
        #         self.bot.cannon(90 + angulo, self.speed)
        #     else:
        #         self.bot.drive(90 + angulo, self.speed)
        #
        # if (location.x > 490 and location.x < 510 and location.y > 480 and location.y < 510):
        #     self.speed = 10
        #     if location.x == 500 and location.y == 500:
        #         self.bot.drive(angulo, 40)
        # else:
        #     self.speed = 100

    def robotDestroyed(self, current=None):
        print("El robot ha sido destruido")

sys.exit(Cliente().main(sys.argv))
