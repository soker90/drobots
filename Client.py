#!/usr/bin/python
# -*- mode:python; coding: utf-8; tab-width -*-

import sys
import Ice
Ice.loadSlice('drobots.ice')
import drobots
import math

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
        game.attach(player)

        self.shutdownOnInterrupt()
        broker.waitForShutdown()

class PlayerI(drobots.Player):

    def __init__(self,adapter):
        self.adapter = adapter

    def makeController(self,bot,current=None):
        RobotControllerServant = RobotControllerI(bot)
        proxyRobotController = self.adapter.addWithUUID(RobotControllerServant)
        return drobots.RobotControllerPrx.uncheckedCast(proxyRobotController)
    def win(self,current=None):
        print("Ganaste")
    def lose(self):
        return 0

class RobotControllerI(drobots.RobotController):
    def __init__(self,bot):
        self.bot = bot
        self.speed = 100
    def turn(self,current=None):
        location = self.bot.location()
        angulo = math.atan(location.y/location.x)*100
        print(location)
        if(location.x == 500):
            if location.y > 500:
                self.bot.drive(270,self.speed)
            else:
                self.bot.drive(90,self.speed)
        elif location.y == 500:
            if location.x > 500:
                self.bot.drive(180,self.speed)
            else:
                self.bot.drive(0,self.speed)
        elif(location.y <500 and location.x <500):
            self.bot.drive(angulo,self.speed)
        elif(location.y >500 and location.x >500):
            self.bot.drive(180+angulo,self.speed)
        elif(location.y >500 and location.x <500):
            self.bot.drive(270+angulo,self.speed)
        elif(location.y <500 and location.x > 500):
            self.bot.drive(90+angulo,self.speed)

        if(location.x  > 490 and location.x < 510 and location.y  > 480 and location.y < 510):
            self.speed = 10
            if location.x == 500 and location.y == 500:
                self.bot.drive(0,0)


    def robotDestroyed(self):
        None

sys.exit(Cliente().main(sys.argv))
