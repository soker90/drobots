#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice

Ice.loadSlice('services.ice --all -I .')
import drobots
import Services

import sys
import Ice
import os

from RobotController import *
from RobotController import RobotControllerAtaque
from RobotController import RobotControllerDefensa


class FactoryI(Services.Factory):
    def make(self, bot, index, current=None):
        sys.stdout.flush()
        print("***Entrando make factory")
        sys.stdout.flush()

        if (bot.ice_isA("::drobots::Attacker")):
            RobotControllerServant = RobotControllerAtaque(bot)
        else:
            RobotControllerServant = RobotControllerDefensa(bot)

        proxyController = current.adapter.addWithUUID(RobotControllerServant)
        directProxy = current.adapter.createDirectProxy(proxyController.ice_getIdentity())
        robotController = drobots.RobotControllerPrx.uncheckedCast(directProxy)

        proxyContainer = current.adapter.getCommunicator().stringToProxy("container")
        container = Services.ContainerPrx.checkedCast(proxyContainer)
        container.linkController(str(index), robotController)

        sys.stdout.flush()
        print("***Saliendo make factory")
        sys.stdout.flush()

        return robotController

    def makeDetector(self, current=None):
        RobotControllerServant = RobotControllerDetector()
        proxyController = current.adapter.addWithUUID(RobotControllerServant)
        directProxy = current.adapter.createDirectProxy(proxyController.ice_getIdentity())
        robotController = drobots.DetectorControllerPrx.checkedCast(directProxy)

        return robotController


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        adapter = broker.createObjectAdapter("FactoryAdapter")
        servant = FactoryI()

        identity = broker.getProperties().getProperty("Identity")
        proxy = adapter.add(servant, broker.stringToIdentity(identity))

        proxyContainer = broker.stringToProxy("container")
        container = Services.ContainerPrx.checkedCast(proxyContainer)

        container.linkFactory(identity[-1], proxy)

        print(container.listFactory())

        print(proxy)
        sys.stdout.flush()

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


if __name__ == '__main__':
    sys.exit(Server().main(sys.argv))
