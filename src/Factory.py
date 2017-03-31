#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('services.ice --all -I .')
import drobots
import Services
from RobotController import *

class Factory(Services.Factory):
    def make(self, bot, current=None):
        print "hola factory"
        if (bot.ice_isA("::drobots::Attacker")):
            RobotControllerServant = RobotControllerAtaque(bot)
        else:
            RobotControllerServant = RobotControllerDefensa(bot)



        proxyController = current.adapter.addWithUUID(RobotControllerServant)
        directProxy = current.adapter.createDirectProxy(proxyController.ice_getIdentity())
        robotController = drobots.RobotControllerPrx.uncheckedCast(directProxy)


        proxy_container = current.adapter.getCommunicator().stringToProxy("container")
        container = Services.ContainerPrx.checkedCast(proxy_container)

        container.link(robotController.ice_getIdentity().name, robotController)

        print robotController

        return robotController


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = Factory()
        adapter = broker.createObjectAdapter("FactoryAdapter")
        identity = broker.getProperties().getProperty("Identity")
        print adapter.add(servant, broker.stringToIdentity(identity))
        sys.stdout.flush()
        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0

if __name__ == '__main__':
    print("hhdhdhd")
    sys.stdout.flush()
    sys.exit(Server().main(sys.argv))
