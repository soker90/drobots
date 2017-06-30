#!/usr/bin/make -f
# -*- mode:makefile -*-

all: start runPlayer runPlayer2

debug: all
	tail -f /tmp/db/node1/out.txt &
	tail -f /tmp/db/node1/err.txt &
	tail -f /tmp/db/node2/out.txt &
	tail -f /tmp/db/node2/err.txt &
	tail -f /tmp/db/node3/out.txt &
	tail -f /tmp/db/node3/err.txt &

start: carpetas deploy
	icegridnode --Ice.Config=node1.config &
	while ! netstat -lptn 2> /dev/null | grep ":4061"; do sleep 1; done
	sleep 1
	icegridnode --Ice.Config=node2.config &
	sleep 1
	icegridnode --Ice.Config=node3.config &
	sleep 2
	icegridadmin --Ice.Config=src/locator.config -u user -p pass -e "application add 'icegrid.xml'" &
	sleep 1
	icegridadmin --Ice.Config=src/locator.config -u user -p pass -e "application update 'icegrid.xml'"

carpetas: /tmp/db/registry /tmp/db/node1/distrib/drobots /tmp/db/node2/distrib/drobots /tmp/db/node3/distrib/drobots 

deploy: /tmp/db/deploy
	cp src/*.py /tmp/db/deploy
	cp *.ice /tmp/db/deploy
	icepatch2calc /tmp/db/deploy


update:
	icegridadmin --Ice.Config=src/locator.config -u user -p pass -e "application update 'icegrid.xml'"

enable-container:
	icegridadmin --Ice.Config=src/locator.config -u user -p pass -e "server enable Container"

enable-factory:
	icegridadmin --Ice.Config=src/locator.config -u user -p pass -e "server enable Factory1"

runPlayer:
	icegridadmin --Ice.Config=src/locator.config -u user -p pass -e "server start Player"

runPlayer2:
	icegridadmin --Ice.Config=src/locator.config -u user -p pass -e "server start Player2"

stop: shutdown clean

shutdown:
	icegridadmin --Ice.Config=src/locator.config -u user -p pass -e "node shutdown node1"
	icegridadmin --Ice.Config=src/locator.config -u user -p pass -e "node shutdown node2"
	icegridadmin --Ice.Config=src/locator.config -u user -p pass -e "node shutdown node3"
	killall icegridnode

startSencillo:
	cd sencillo && make run12

/tmp/db/%:
	mkdir -p $@

clean:
	rm -rf /tmp/db
	rm -rf src/*~
	rm -rf src/*.pyc
	
