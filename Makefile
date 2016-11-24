#!/usr/bin/make -f
# -*- mode:makefile -*-

run: 
	./Client.py --Ice.Config=client.config 'drobots1 -t -e 1.1:tcp -h atclab.esi.uclm.es -p 4061'
run1: 
	./Client.py --Ice.Config=client.config 'drobots1'
run2: 
	./Client.py --Ice.Config=client.config 'drobots2'
run3: 
	./Client.py --Ice.Config=client.config 'drobots3'
run4: 
	./Client.py --Ice.Config=client.config 'drobots4'
run5: 
	./Client.py --Ice.Config=client.config 'drobots5'
run6: 
	./Client.py --Ice.Config=client.config 'drobots6'
run7: 
	./Client.py --Ice.Config=client.config 'drobots7'
run8: 
	./Client.py --Ice.Config=client.config 'drobots8'
run9: 
	./Client.py --Ice.Config=client.config 'drobots9'

start: /tmp/db/registry /tmp/db/node1
	icegridnode --Ice.Config=src/node1.config &

stop:
	icegridadmin --Ice.Config=src/locator.config -u user -p pass -e "node shutdown node1";
	killall icegridnode

/tmp/db/%:
	mkdir -p $@

clean:
	rm *~
	rm -r /tmp/db
