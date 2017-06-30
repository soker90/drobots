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

        nick = ''.join(random.choice('qwertyuiopasdfghjkl') for _ in range(3))

        playerServant = PlayerI(container, nick)
        proxyPlayer = adapter.addWithUUID(playerServant)
        proxyPlayerId = proxyPlayer.ice_getIdentity()
        proxyDirectPlayer = adapter.createDirectProxy(proxyPlayerId)

        player = drobots.PlayerPrx.checkedCast(proxyDirectPlayer)

        proxyGame = broker.propertyToProxy("Game")
        game = drobots.GamePrx.checkedCast(proxyGame)
        #proxyGame = broker.propertyToProxy("Private")
        #gameFactory = drobots.GameFactoryPrx.checkedCast(proxyGame)
        #game = gameFactory.makeGame("Eduardo22", 2)



        try:
            print('Haciendo login')
            game.login(player, nick)
            print('Esperando robots')
        except drobots.GameInProgress:
            print("Partida en curso.")
        except drobots.InvalidProxy:
            print("Proxy inválido")
        except drobots.InvalidName as e:
            print("Nombre inválido")
            print(str(e.reason))
        except drobots.BadNumberOfPlayers:
            print("Número de jugadores no válidos")

        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


class PlayerI(drobots.Player):

    def __init__(self, container, nick, current=None):
        self.nick = nick
        self.i = 1
        self.detectores = 1
        self.factorias = container.listFactory()


    def makeController(self, bot, current=None):
        print("PLAYER: Entrando makecontroller")
        sys.stdout.flush()

        index = self.nick + str(self.i)

        if bot.ice_isA("::drobots::Robot"):
            factoria = 1
            sys.stdout.flush()
        elif (bot.ice_isA("::drobots::Attacker")):
            factoria = 2
        elif(bot.ice_isA("::drobots::Defender")):
            factoria = 3

        proxy = self.factorias[str(factoria)]
        factory = Services.FactoryPrx.checkedCast(proxy)
        robotController = factory.make(bot, index)

        self.i = self.i + 1

        print("PLAYER: RobotController -> "+str(robotController))
        sys.stdout.flush()
        print("PLAYER: Saliendo makeController")
        sys.stdout.flush()

        return robotController


    def makeDetectorController(self, current=None):
        print("PLAYER: Entrando makeDetectorcontroller")
        sys.stdout.flush()
        proxy = self.factorias[str(1)]
        factory = Services.FactoryPrx.checkedCast(proxy)

        index = self.nick + str(self.i)
        robotController = factory.makeDetector(index)

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
