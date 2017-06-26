#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('services.ice --all -I .')
import drobots
import Services
from RobotController import *
from RobotController import RobotControllerAtaque
from RobotController import RobotControllerDefensa

class FactoryI(Services.Factory):
    def make(self, bot, current=None):
        print( "hola factory")

        if (bot.ice_isA("::drobots::Attacker")):
            RobotControllerServant = RobotControllerAtaque(bot)
        else:
            RobotControllerServant = RobotControllerDefensa(bot)


        proxyController = current.adapter.addWithUUID(RobotControllerServant)
        directProxy = current.adapter.createDirectProxy(proxyController.ice_getIdentity())
        robotController = drobots.RobotControllerPrx.checkedCast(directProxy)

        print("fin factory")
        return robotController

    def makeDetector(self, container_robots, current=None):

        return 0


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        adapter = broker.createObjectAdapter("FactoryAdapter")
        servant = FactoryI()


        identity = broker.getProperties().getProperty("Identity")
        proxy = adapter.add(servant, broker.stringToIdentity(identity))

        print(proxy)
        sys.stdout.flush()

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0

if __name__ == '__main__':
    sys.exit(Server().main(sys.argv))
