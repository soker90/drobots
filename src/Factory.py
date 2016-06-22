# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('drobots.ice')
import drobots
Ice.loadSlice('-I %s container.ice' % Ice.getSliceDir())
from RobotController import *

class ControllerFactoryI(drobots.ControllerFactory):
    def __init__(self):
        pass

    def make(self, bot, container, key, current=None):

        if (bot.ice_isA("::drobots::Attacker")):
            RobotControllerServant = RobotControllerAtaque(bot,container)
            proxy = current.adapter.addWithUUID(RobotControllerServant)
            container.link(key,proxy)
        elif (bot.ice_isA("::drobots::Defender")):
            RobotControllerServant = RobotControllerDefensa(bot,container)

        proxy = current.adapter.addWithUUID(RobotControllerServant)
        container.link(key,proxy)
        return drobots.RobotControllerPrx.uncheckedCast(proxy)


class ServerFactory(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        adapter = broker.createObjectAdapter("FactoryAdapter")
        servant = ControllerFactoryI()
        proxy = adapter.add(servant, broker.stringToIdentity("factory"))

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


factory = ServerFactory()
sys.exit(factory.main(sys.argv))
