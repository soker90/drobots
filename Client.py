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

        playerServant = PlayerI()
        proxyPlayer = adapter.addWithUUID(playerServant)
        player=drobots.PlayerPrx.checkedCast(proxyPlayer)

        proxyGame = broker.stringToProxy(argv[1])
        game = drobots.GamePrx.checkedCast(proxyGame)

        adapter.activate()
        nick = ''.join(random.choice('qwertyuiopasdfghjkl') for _ in range(3))
        game.login(player,nick)

        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return playerServant.salida


class PlayerI(drobots.Player):

    def __init__(self):
        pass

    def win(self,current=None):
        print("Has ganado")
        self.salida = 0
        current.adapter.getCommunicator().shutdown()

    def lose(self, current=None):
        print("Has perdido")
        self.salida = 1
        current.adapter.getCommunicator().shutdown()
        
    def gameAbort(self, current=None):
        print('Juego Abortado. Saliendo...')
        self.salida = 1
        current.adapter.getCommunicator().shutdown()

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
        pass


sys.exit(Cliente().main(sys.argv))
