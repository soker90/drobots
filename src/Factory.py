# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('drobots.ice')
import drobots
Ice.loadSlice('services.ice')
import Services
from RobotController import *

class FactoryI(Services.Factory):
    def make(self, key, current=None):
        pass

        #if (bot.ice_isA("::drobots::Attacker")):
        #    RobotControllerServant = RobotControllerAtaque(bot,container)
        #    proxy = current.adapter.addWithUUID(RobotControllerServant)
        #    container.link(key,proxy)
        #elif (bot.ice_isA("::drobots::Defender")):
        #    RobotControllerServant = RobotControllerDefensa(bot,container)

        #proxy = current.adapter.addWithUUID(RobotControllerServant)
        #container.link(key,proxy)
        #return drobots.RobotControllerPrx.uncheckedCast(proxy)

##Crear interfaz ice

class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = FactoryI()
        adapter = broker.createObjectAdapter("FactoryAdapter")
        adapter.add(servant, broker.stringToIdentity("factory1"))

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0

if __name__ == '__main__':
    sys.exit(Server().main(sys.argv))
