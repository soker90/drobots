#!/usr/bin/make -f
# -*- mode:makefile -*-

debug: start runPlayer
	tail -f /tmp/db/node1/out.txt &
	tail -f /tmp/db/node1/err.txt &

start: /tmp/db/registry /tmp/db/node1
	icegridnode --Ice.Config=src/node1.config &
	sleep 3
	icegridadmin --Ice.Config=src/locator.config -u user -p pass -e "application add 'icegrid.xml'" &
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

startSencillo:
	cd sencillo && make run12

/tmp/db/%:
	mkdir -p $@

clean:
	rm -rf /tmp/db
	rm -rf src/*~
	rm -rf src/*.pyc
	
