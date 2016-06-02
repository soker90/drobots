#!/usr/bin/python -u

import sys
import Ice
Ice.loadSlice('container.ice')
import Services


class ContainerI(Services.Container):
    def __init__(self):
        self.proxies = {}

    def link(self, key, proxy, current=None):
        if key in self.proxies:
            raise Services.AlreadyExists(key)

        print("link: {0} -> {1}".format(key, proxy))
        self.proxies[key] = proxy

    def unlink(self, key, current=None):
        if not key in self.proxies:
            raise Services.NoSuchKey(key)

        print("unlink: {0}".format(key))
        del self.proxies[key]

    def list(self, current=None):
        return self.proxies
