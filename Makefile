#!/usr/bin/make -f
# -*- mode:makefile -*-

run: 
	./Client.py --Ice.Config=client.config 'drobots -t -e 1.1:tcp -h atclab.esi.uclm.es -p 10000 -t 60000'

clean:
	rm *~
