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
from RobotController import *

class Cliente(Ice.Application):
    def run(self, argv):

        broker = self.communicator()

        adapter = broker.createObjectAdapter('PlayerAdapter')
        adapter.activate()

        servantContainer = Container.ContainerI()
        proxyContainer = adapter.addWithUUID(servantContainer)

        playerServant = PlayerI(str(proxyContainer),broker)
        proxyPlayer = adapter.addWithUUID(playerServant)


        player=drobots.PlayerPrx.checkedCast(proxyPlayer)

        proxyGame = broker.stringToProxy(argv[1])
        game = drobots.GamePrx.checkedCast(proxyGame)


        nick = ''.join(random.choice('qwertyuiopasdfghjkl') for _ in range(3))
        game.login(player,nick)
        print("Entrado en el juego")

        self.shutdownOnInterrupt()
        broker.waitForShutdown()

class PlayerI(drobots.Player):

    def __init__(self,proxyContainer,broker):
        self.broker = broker
        self.i = 1
        self.proxyContainer = proxyContainer
        self.container = self.crear_container()


    def makeController(self,bot,current=None):
        if (bot.ice_isA("::drobots::Attacker")):
            RobotControllerServant = RobotControllerAtaque(bot,self.container)
        elif (bot.ice_isA("::drobots::Defender")):
            RobotControllerServant = RobotControllerDefensa(bot,self.container)
        proxyRobotController = current.adapter.addWithUUID(RobotControllerServant)
        if(RobotControllerServant.getTipo() == "defensa"):
            self.container.link(str(self.i),proxyRobotController)
            self.i += 1
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




sys.exit(Cliente().main(sys.argv))
