#!/usr/bin/make -f
# -*- mode:makefile -*-

start-grid: /tmp/db/registry /tmp/db/node1 /tmp/db/node2
	icegridnode --Ice.Config=src/node1.config &
	icegridnode --Ice.Config=src/node2.config &

stop-grid:
		for node in node1; do \
	    	icegridadmin --Ice.Config=src/node1.config -uuser -ppass -e "node shutdown $$node"; \
	done
	killall icegridnode

/tmp/db/%:
	mkdir -p $@

clean: stop-grid
	rm *~
	rm -r /tmp/db
