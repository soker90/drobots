#!/usr/bin/make -f
# -*- mode:makefile -*-

run: 
	./Client.py --Ice.Config=client.config 'drobots0'
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


clean:
	rm *~
