#!/usr/bin/make -f
# -*- mode:makefile -*-

N1 = node1
N2 = node2
N3 = node3
N4 = node4
C1 = node1.config
C2 = node2.config
C3 = node3.config
C4 = node4.config

start: /tmp/db/registry /tmp/db/node1 /tmp/db/node2 /tmp/db/node3 /tmp/db/node4
	icegridnode --Ice.Config=src/node1.config &
	icegridnode --Ice.Config=src/node2.config &
	icegridnode --Ice.Config=src/node3.config &
	icegridnode --Ice.Config=src/node4.config &

stop:
	icegridadmin --Ice.Config=src/locator.config -u user -p pass -e "node shutdown node1";
	icegridadmin --Ice.Config=src/locator.config -u user -p pass -e "node shutdown node2";
	icegridadmin --Ice.Config=src/locator.config -u user -p pass -e "node shutdown node3";
	icegridadmin --Ice.Config=src/locator.config -u user -p pass -e "node shutdown node4";
	killall icegridnode

/tmp/db/%:
	mkdir -p $@

clean: stop-grid
	rm *~
	rm -r /tmp/db
