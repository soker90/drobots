#!/usr/bin/python
# -*- mode:python; coding: utf-8; tab-width -*-

import sys
import Ice
Ice.loadSlice('drobots.ice')
import drobots

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
        game.login(player,"miplayer")

        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return playerServant.salida


class PlayerI(drobots.Player):

    def __init__(self):
        pass

    def getID(self,current=None):
        return "06280339M"

    def win(self,current=None):
        print("Has ganado")
        self.salida = 0
        current.adapter.getCommunicator().shutdown()

    def lose(self, current=None):
        print("Has perdido")
        self.salida = 1
        current.adapter.getCommunicator().shutdown()


sys.exit(Cliente().main(sys.argv))
