#!/usr/bin/make -f
# -*- mode:makefile -*-

start: /tmp/db/registry /tmp/db/node1
	icegridnode --Ice.Config=src/node1.config &
	sleep 3
	icegridadmin --Ice.Config=src/locator.config -u user -p pass -e "application add 'icegrid.xml'"
	sleep 1
	icegridadmin --Ice.Config=src/locator.config -u user -p pass -e "application update 'icegrid.xml'"

update:
	icegridadmin --Ice.Config=src/locator.config -u user -p pass -e "application update 'icegrid.xml'"

enable-container:
	icegridadmin --Ice.Config=src/locator.config -u user -p pass -e "server enable Container"

enable-factory:
	icegridadmin --Ice.Config=src/locator.config -u user -p pass -e "server enable Factory1"

runPlayer:
	icegridadmin --Ice.Config=src/locator.config -u user -p pass -e "server start Player"

stop: shutdown clean

shutdown:
	icegridadmin --Ice.Config=src/locator.config -u user -p pass -e "node shutdown node1"
	killall icegridnode

/tmp/db/%:
	mkdir -p $@

clean:
	rm -rf /tmp/db
	rm -rf *~
	
