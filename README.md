# DROBOTS

El juego está orquestado por un servidor que crea partidas a la que se conectan los jugadores. Los jugadores aportan controladores de robots y, opcionalmente, controladores de detectores. Cuando la partida dispone del número de jugadores adecuado, crea robots y detectores para cada jugador y les solicita los controladores para los mismos. Todos ellos: servidor, jugador, robot y controladores son objetos distribuidos.

Después, el juego va indicando a cada controlador de robot un turno en el que puede interaccionar con el robot asociado. 

## Instalación

### En Ubuntu

```sh
apt-key adv --keyserver keyserver.ubuntu.com --recv 5E6DA83306132997
apt-add-repository "deb http://zeroc.com/download/apt/ubuntu$(lsb_release -rs) stable main"
apt-get update
apt-get install zeroc-ice-all-runtime zeroc-ice-all-dev git
cd ~ && wget http://arco.esi.uclm.es/~joseluis.segura/python-zeroc-ice/ubuntu/16.04/python3-zeroc-ice36_3.6.2.1-6_amd64.deb
dpkg -i python3-zeroc-ice36_3.6.2.1-6_amd64.deb
```


### En Archlinux

```sh
yaourt -S zeroc-ice python-zeroc-ice git
```

## Ejecución

```sh
make
```

### Debug

Para ejecutarlo y ver las salidas para debug

```sh
make debug
```

## Licencia

GPLv3
