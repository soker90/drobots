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

from RobotController import RobotControllerAtaque
from RobotController import RobotControllerDefensa
from RobotController import RobotController
from DetectorController import RobotControllerDetector


class FactoryI(Services.Factory):
    def make(self, bot, index, current=None):
        sys.stdout.flush()
        print("FACTORY: Entrando make")
        sys.stdout.flush()

        if bot.ice_isA("::drobots::Attacker") and bot.ice_isA("::drobots::Defender"):
            RobotControllerServant = RobotController(bot, index)
            print("FACTORY: Robot Completo")
            index = index+"C"
            sys.stdout.flush()
        elif (bot.ice_isA("::drobots::Attacker")):
            RobotControllerServant = RobotControllerAtaque(bot, index)
            print("FACTORY: Robot Atacante")
            index = index + "A"
            sys.stdout.flush()
        else:
            RobotControllerServant = RobotControllerDefensa(bot, index)
            print("FACTORY: Robot Defensor")
            sys.stdout.flush()
            index = index + "D"




        proxyController = current.adapter.addWithUUID(RobotControllerServant)
        directProxy = current.adapter.createDirectProxy(proxyController.ice_getIdentity())
        robotController = drobots.RobotControllerPrx.checkedCast(directProxy)

        proxyContainer = current.adapter.getCommunicator().stringToProxy("container")
        container = Services.ContainerPrx.checkedCast(proxyContainer)
        container.linkController(str(index), robotController)

        RobotControllerServant.setContainer(proxyContainer)

        sys.stdout.flush()
        print("FACTORY: Saliendo make")
        sys.stdout.flush()

        return robotController

    def makeDetector(self, index, current=None):
        print("FACTORY: Entrando makeDetector")
        sys.stdout.flush()
        DetectorControllerServant = RobotControllerDetector()
        proxyController = current.adapter.addWithUUID(DetectorControllerServant)
        directProxy = current.adapter.createDirectProxy(proxyController.ice_getIdentity())
        robotController = drobots.DetectorControllerPrx.checkedCast(directProxy)

        index = index + "X"

        proxyContainer = current.adapter.getCommunicator().stringToProxy("container")
        container = Services.ContainerPrx.checkedCast(proxyContainer)
        container.linkController(str(index), robotController)

        print("FACTORY: Saliendo makeDetector")
        sys.stdout.flush()
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
