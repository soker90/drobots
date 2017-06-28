#!/usr/bin/python3 -u
# -*- coding:utf-8; tab-width:4; mode:python -*-

import sys
import Ice
Ice.loadSlice('services.ice --all -I .')
import Services


class ContainerI(Services.Container):
    def __init__(self):
        self.proxies = {}
        self.proxiesFactory = {}
        self.proxiesController = {}

    def link(self, key, proxy, current=None):
        if key in self.proxies:
            raise Services.AlreadyExists(key)

        print("CONTAINER: link: {0} -> {1}".format(key, proxy))
        self.proxies[key] = proxy

    def linkFactory(self, key, proxy, current=None):
        if key in self.proxiesFactory:
            raise Services.AlreadyExists(key)

        print("CONTAINER: linkFactoria: {0} -> {1}".format(key, proxy))
        self.proxiesFactory[key] = proxy

    def linkController(self, key, proxy, current=None):
        if key in self.proxiesController:
            raise Services.AlreadyExists(key)

        print("CONTAINER: linkController: {0} -> {1}".format(key, proxy))
        self.proxiesController[key] = proxy

    def unlink(self, key, current=None):
        if not key in self.proxies:
            raise Services.NoSuchKey(key)

        print("CONTAINER: unlink: {0}".format(key))
        del self.proxies[key]

    def list(self, current=None):
        return self.proxies

    def listFactory(self, current=None):
        return self.proxiesFactory

    def listController(self, current=None):
        return self.proxiesController


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = ContainerI()

        adapter = broker.createObjectAdapter("ContainerAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("container"))

        print(proxy)

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


if __name__ == '__main__':
    sys.exit(Server().main(sys.argv))