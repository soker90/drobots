#!/usr/bin/python
# -*- mode:python; coding: utf-8; tab-width -*-

import sys
import Ice
Ice.loadSlice('drobots.ice')
import drobots
Ice.loadSlice('-I %s container.ice' % Ice.getSliceDir())
import Services
import math
import random
import Container

class Cliente(Ice.Application):
    def run(self, argv):

        broker = self.communicator()

        adapter = broker.createObjectAdapter('PlayerAdapter')
        adapter.activate()

        servantContainer = Container.ContainerI()
        proxyContainer = adapter.addWithUUID(servantContainer) #adapter.add(servantContainer, broker.stringToIdentity('container1')) #

        print(proxyContainer)

        playerServant = PlayerI(str(proxyContainer),broker)
        proxyPlayer = adapter.addWithUUID(playerServant)


        player=drobots.PlayerPrx.checkedCast(proxyPlayer)

        proxyGame = broker.stringToProxy(argv[1])
        game = drobots.GamePrx.checkedCast(proxyGame)


        nick = ''.join(random.choice('qwertyuiopasdfghjkl') for _ in range(3))
        game.login(player,nick)

        self.shutdownOnInterrupt()
        broker.waitForShutdown()

class PlayerI(drobots.Player):

    def __init__(self,proxyContainer,broker):
        self.broker = broker
        self.proxyContainer = proxyContainer
        self.container = self.crear_container()


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
    def gameAbort(self, current=None):
        print("Juego cancelado")
        current.adapter.getCommunicator().shutdown()

    def crear_container(self):
        proxy = self.broker.stringToProxy(self.proxyContainer)
        container = Services.ContainerPrx.checkedCast(proxy)
        return container

class RobotControllerAtaque(drobots.RobotController):
    def __init__(self,bot):
        self.bot = bot
        self.speed = 100
        self.i = 0

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

    def turn(self,current=None):
        location = self.bot.location()
        angulo = math.atan(location.y/location.x)
        if(self.i%2==0):
            self.bot.cannon(angulo, self.speed)
        else:
            self.mover(location, angulo)

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
        self.danyo = 0

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



    def robotDestroyed(self, current=None):
        print("El robot ha sido destruido")


sys.exit(Cliente().main(sys.argv))
