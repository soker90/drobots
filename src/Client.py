#!/usr/bin/python
# -*- mode:python; coding: utf-8; tab-width -*-

import sys
import Ice
Ice.loadSlice('services.ice --all -I .')
import drobots
import Services
import math
import random
import Container
from RobotController import *
from Factory import *

class Cliente(Ice.Application):
    def run(self, argv):

        broker = self.communicator()

        adapter = broker.createObjectAdapter('PlayerAdapter')
        adapter.activate()

        playerServant = PlayerI(broker)
        proxyPlayer = adapter.addWithUUID(playerServant)
        prx_id = proxyPlayer.ice_getIdentity()
        direct_prx = adapter.createDirectProxy(prx_id)


        player=drobots.PlayerPrx.checkedCast(direct_prx)

        proxyGame = broker.propertyToProxy("Game")
        #proxyGame = broker.stringToProxy('drobots3')
        game = drobots.GamePrx.checkedCast(proxyGame)


        nick = ''.join(random.choice('qwertyuiopasdfghjkl') for _ in range(3))

        try:
            print 'Haciendo login'
            game.login(player,nick)
            print 'Esperando robots'
        except drobots.GameInProgress:
            print "Partida en curso."
        except drobots.InvalidProxy:
            print "Proxy inválido"
        except drobots.InvalidName:
            print "Nombre inválido"

        self.shutdownOnInterrupt()
        broker.waitForShutdown()

class PlayerI(drobots.Player):

    def __init__(self,broker):
        self.broker = broker
        self.i = 1
        self.container = self.crear_container()


    def makeController(self,bot,current=None):
        if (bot.ice_isA("::drobots::Attacker")):
            tipo = 0
        elif (bot.ice_isA("::drobots::Defender")):
            tipo = 1

        proxy = self.broker.stringToProxy("factory1")
        factory = Services.FactoryPrx.checkedCast(proxy)
        print "llega"
        robot = factory.make(tipo)
        print("robot" + robot)
        self.i = self.i + 1
        return robot


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
        proxy = self.broker.stringToProxy("container")
        container = Services.ContainerPrx.checkedCast(proxy)
        return container




sys.exit(Cliente().main(sys.argv))
