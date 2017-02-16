#!/usr/bin/python
# -*- mode:python; coding: utf-8; tab-width -*-

import sys
import Ice
Ice.loadSlice('drobots.ice')
Ice.loadSlice('services.ice --all -I .')
import drobots
import math
import random
import Container
from RobotController import *
from Factory import *
import Services

class Cliente(Ice.Application):
    def run(self, argv):
        broker = self.communicator()

        adapter = broker.createObjectAdapter('PlayerAdapter')
        adapter.activate()

        playerServant = PlayerI()
        proxyPlayer = adapter.addWithUUID(playerServant)
        proxyPlayerId = proxyPlayer.ice_getIdentity()
        proxyDirectPlayer = adapter.createDirectProxy(proxyPlayerId)

        player = drobots.PlayerPrx.checkedCast(proxyDirectPlayer)

        proxyGame = broker.propertyToProxy("Game")
        game = drobots.GamePrx.checkedCast(proxyGame)

        nick = ''.join(random.choice('qwertyuiopasdfghjkl') for _ in range(3))

        try:
            print('Haciendo login')
            game.login(player, nick)
            print('Esperando robots')
        except drobots.GameInProgress:
            print("Partida en curso.")
        except drobots.InvalidProxy:
            print("Proxy inválido")
        except drobots.InvalidName:
            print("Nombre inválido")

        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return playerServant.salida


class PlayerI(drobots.Player):

    def __init__(self):
        self.salida = 1
        self.i = 1
        #proxy = current.adapter.getCommunicator().stringToProxy("container")
        #self.container = Services.ContainerPrx.checkedCast(proxy)


    def makeController(self, bot, current=None):
        proxy = current.adapter.getCommunicator().stringToProxy("factory1")
        factory = Services.FactoryPrx.checkedCast(proxy)
        robotController = factory.make(bot)
        self.i = self.i + 1
        return robotController

    def makeDetectorController(self, current=None):
        print "detectores"

    def win(self,current=None):
        print("Has ganado")
        self.salida = 0
        current.adapter.getCommunicator().shutdown()

    def lose(self, current=None):
        print("Has perdido")
        current.adapter.getCommunicator().shutdown()

    def gameAbort(self, current=None):
        print('Juego Abortado. Saliendo...')
        current.adapter.getCommunicator().shutdown()


sys.exit(Cliente().main(sys.argv))
