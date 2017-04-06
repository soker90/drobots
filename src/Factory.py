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
    def make(self, bot, id, current=None):
        print( "hola factory")

        if (bot.ice_isA("::drobots::Attacker")):
            RobotControllerServant = RobotControllerAtaque(bot, id)
        else:
            RobotControllerServant = RobotControllerDefensa(bot, id)


        proxyController = current.adapter.addWithUUID(RobotControllerServant)
        directProxy = current.adapter.createDirectProxy(proxyController.ice_getIdentity())
        robotController = drobots.RobotControllerPrx.checkedCast(directProxy)


        #proxy_container = current.adapter.getCommunicator().stringToProxy("container")
        #container = Services.ContainerPrx.checkedCast(proxy_container)

        #container.link(robotController.ice_getIdentity().name, robotController)


        return robotController
    def makeDetector(self, current = None):
        print("Detector Factory")


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()

        adapter = broker.createObjectAdapter("FactoryAdapter")
        identity = broker.getProperties().getProperty("Identity")
        servant = FactoryI()
        proxy = adapter.add(servant, broker.stringToIdentity(identity))
        print(proxy)
        sys.stdout.flush()

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0

sys.exit(Server().main(sys.argv))
