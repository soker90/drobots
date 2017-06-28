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
from DetectorController import *

class Cliente(Ice.Application):
    def run(self, argv):
        broker = self.communicator()

        adapter = broker.createObjectAdapter('PlayerAdapter')
        adapter.activate()

        proxy = broker.stringToProxy("container")
        container = Services.ContainerPrx.checkedCast(proxy)

        playerServant = PlayerI(container)
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

    def __init__(self, container, current=None):
        self.factoria = 1
        self.i = 1
        self.detectores = 1
        self.container = container


    def makeController(self, bot, current=None):
        print("PLAYER: Entrando makecontroller")
        sys.stdout.flush()

        factorias = self.container.listFactory()
        proxy = factorias[str(self.factoria)]
        factory = Services.FactoryPrx.checkedCast(proxy)
        robotController = factory.make(bot, self.i)

        #proxy = current.adapter.getCommunicator().stringToProxy("factory"+str(self.factoria))
        #factory = Services.FactoryPrx.checkedCast(proxy)
        #robotController = factory.make(bot)


        #if (bot.ice_isA("::drobots::Attacker")):
        #    RobotControllerServant = RobotControllerAtaque(bot)
        #else:
        #    RobotControllerServant = RobotControllerDefensa(bot)
        self.i = self.i + 1


        #self.factoria += 1
        print("PLAYER: RobotController -> "+str(robotController))
        sys.stdout.flush()
        print("PLAYER: Saliendo makeController")
        sys.stdout.flush()

        return robotController


    def makeDetectorController(self, current=None):
        print("PLAYER: Entrando makeDetectorcontroller")
        sys.stdout.flush()
        factorias = self.container.listFactory()
        proxy = factorias[str(self.factoria)]
        factory = Services.FactoryPrx.checkedCast(proxy)
        robotController = factory.makeDetector(self.i)

        self.i = self.i + 1
        print("PLAYER: Saliendo makeDetectorcontroller")
        sys.stdout.flush()

        return robotController

    def win(self, current=None):
        print("Has ganado")
        current.adapter.getCommunicator().shutdown()

    def lose(self, current=None):
        print("Has perdido")
        current.adapter.getCommunicator().shutdown()

    def gameAbort(self, current=None):
        print('Juego Abortado. Saliendo...')
        current.adapter.getCommunicator().shutdown()


sys.exit(Cliente().main(sys.argv))
