#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('services.ice')
import Services
Ice.loadSlice('drobots.ice')
import drobots
from RobotController import *

class FactoryI(Services.Factory):
    def make(self, tipo, current=None):
        if (tipo == 0):
            RobotControllerServant = RobotControllerAtaque()
        else:
            RobotControllerServant = RobotControllerDefensa()

        proxyController = current.adapter.addWithUUID(RobotControllerServant)
        directProxy = current.adapter.createDirectProxy(proxyController.ice_getIdentity())
        robotController = drobots.RobotControllerPrx.uncheckedCast(directProxy)


        proxy_container = current.adapter.stringToProxy("container")
        container = Services.ContainerPrx.checkedCast(proxy_container)

        container.link(robotController.ice_getIdentity().name, robotController)

        return robotController


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = FactoryI()
        adapter = broker.createObjectAdapter("FactoryAdapter")
        adapter.add(servant, broker.stringToIdentity("factory"))

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0

if __name__ == '__main__':
    sys.exit(Server().main(sys.argv))
