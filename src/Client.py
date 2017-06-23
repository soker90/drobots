#!/usr/bin/python3
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
import Services
from Factory import *

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

        return 0


class PlayerI(drobots.Player):

    def __init__(self):
        self.factorias = 1
        self.i = 1
        self.detectores = 1
        #proxy = current.adapter.getCommunicator().stringToProxy("container")
        #self.container = Services.ContainerPrx.checkedCast(proxy)


    def makeController(self, bot, current=None):

        #proxy = current.adapter.getCommunicator().stringToProxy("factory1")
        #print(proxy)
        #factory = Services.FactoryPrx.checkedCast(proxy)
        #robotController = factory.make(bot)

        proxyContainer = current.adapter.getCommunicator().stringToProxy("container")
        container = Services.ContainerPrx.checkedCast(proxyContainer)

        if (bot.ice_isA("::drobots::Attacker")):
            tipo = "Atacante"
        else:
            tipo = "Defensor"

        #container.link(tipo + str(self.i), robotController)
        print(tipo)

        self.i = self.i + 1

        self.factorias += 1

        #return robotController


    def makeDetectorController(self, current=None):
        print("detectores")

    def win(self,current=None):
        print("Has ganado")
        current.adapter.getCommunicator().shutdown()

    def lose(self, current=None):
        print("Has perdido")
        current.adapter.getCommunicator().shutdown()

    def gameAbort(self, current=None):
        print('Juego Abortado. Saliendo...')
        current.adapter.getCommunicator().shutdown()


sys.exit(Cliente().main(sys.argv))
