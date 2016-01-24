#!/usr/bin/make -f
# -*- mode:makefile -*-

all:

clean:
	$(RM) *~ *.pyc

run-client1:
	./Client.py --Ice.Config=locator.config 'drobots1'

run-client2:
	./Client.py --Ice.Config=locator.config 'drobots2'

run-client3:
	./Client.py --Ice.Config=locator.config 'drobots3'

run-client4:
	./Client.py --Ice.Config=locator.config 'drobots4'

run-client5:
	./Client.py --Ice.Config=locator.config 'drobots5'

run-client6:
	./Client.py --Ice.Config=locator.config 'drobots6'

run-client7:
	./Client.py --Ice.Config=locator.config 'drobots7'

run-examen:
	./Client.py --Ice.Config=locator.config 'drobotsexam'
