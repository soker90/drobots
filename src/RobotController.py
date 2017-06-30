#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('-I. --all drobots.ice')
Ice.loadSlice('services.ice --all -I .')
import drobots
import math
import random
import Container
import Services
import math
import random


class RobotControllerAtaque(Services.AttackerController):
    def __init__(self, bot, key, current=None):
        self.bot = bot
        self.key = key
        self.container = None
        self.listAttaker = []
        self.listDefender = []
        self.listCompleto = []
        self.listDetector = []
        self.firstTime = True
        self.location = None
        self.energia = 0
        self.velocidad = 0

    def setLists(self):
        controllers = self.container.listController()
        for key in controllers.keys():
            if key != self.key and key[:3] == self.key[:3]:
                if key[-1] == "D":
                    controller = Services.DefenderControllerPrx.checkedCast(controllers[key])
                    self.listDefender.append(controller)
                elif key[-1] == "A":
                    controller = Services.AttackerControllerPrx.checkedCast(controllers[key])
                    self.listAttaker.append(controller)
                elif key[-1] == "C":
                    controller = Services.CompletoControllerPrx.checkedCast(controllers[key])
                    self.listCompleto.append(controller)
                elif key[-1] == "X":
                    print("detector")
                    sys.stdout.flush()
                    controller = Services.DetectorControllerIPrx.checkedCast(controllers[key])
                    self.listDetector.append(controller)

    def turn(self, current=None):
        print("ATACANTE " + self.key + ": Jugador " + self.key[:3])
        sys.stdout.flush()
        self.energia = 100
        if self.firstTime:
            self.setLists()
        self.firstTime = False

        self.location = self.bot.location()
        self.energia -= 1
        self.shoot(1)

        if self.energia >= 60:
            self.mover()

    def shoot(self, cont, current=None):
        if cont > 5:
            return None
        print("ATACANTE " + self.key + ": Disparando")
        sys.stdout.flush()
        nlista = random.randint(1, 3)

        if nlista == 1:
            lista = self.listDefender
        elif nlista ==2:
            lista = self.listCompleto
        elif nlista == 3:
            lista = self.listDetector

        controller = lista.pop(0)
        enemigoX = controller.getEnemigoX()
        enemigoY = controller.getEnemigoY()
        lista.append(controller)

        if len(lista) > 1:
            if enemigoY < 0 or enemigoX < 0:
                print("ATACANTE " + self.key + ": Disparo Cancelado")
                sys.stdout.flush()
                self.shoot(cont + 1)

        if enemigoY > -1 and enemigoX > -1:
            print("enemigo X:" + str(enemigoX) + " Y:" + str(enemigoY))
            x = enemigoX - self.location.x
            y = enemigoY - self.location.y
            angulo = int(math.degrees(math.atan2(y, x)))
            if angulo < 0:
                angulo += 360
            elif angulo >= 360:
                angulo -= 360

            distancia = random.randint(1, 50) * 10
            if not self.isAmigo(angulo, distancia):
                self.bot.cannon(angulo, distancia)
                self.energia -= 50
            else:
                print("ATACANTE " + self.key + ": Amigo cerca, disparo Cancelado")
                sys.stdout.flush()
                self.shoot(cont + 1)


    def isAmigo(self, anguloEnemigo, distancia):
        x = self.location.x + math.cos(anguloEnemigo) * distancia
        y = self.location.y + math.sin(anguloEnemigo) * distancia
        for i in self.listDefender:
            pos = i.posicion()

            if math.fabs(pos.x - x) < 50 and math.fabs(pos.y - y) < 50:
                return True

        for i in self.listAttaker:
            pos = i.posicion()

            if math.fabs(pos.x - x) < 50 and math.fabs(pos.y - y) < 50:
                return True

        for i in self.listCompleto:
            pos = i.posicion()

            if math.fabs(pos.x - x) < 50 and math.fabs(pos.y - y) < 50:
                return True

        return False

    def mover(self):
        print("ATACANTE " + self.key + ": Moviendo robot")
        sys.stdout.flush()
        if (self.velocidad == 0):
            self.bot.drive(random.randint(0, 360), 100)
            self.velocidad = 100
        elif (self.location.x > 300):
            self.bot.drive(225, 49)
            self.velocidad = 49
        elif (self.location.x < 30):
            self.bot.drive(45, 49)
            self.velocidad = 49
        elif (self.location.y > 300):
            self.bot.drive(315, 49)
            self.velocidad = 49
        elif (self.location.y < 30):
            self.bot.drive(135, 49)
            self.velocidad = 49
        self.energia -= 60


    def setContainer(self, proxy):
        self.container = Services.ContainerPrx.checkedCast(proxy)

    def posicion(self, current=None):
        pos = self.bot.location()
        return pos

    def robotDestroyed(self, current=None):
        print("ATACANTE " + self.key + ": Robot destruido")
        sys.stdout.flush()

class RobotControllerDefensa(Services.DefenderController):
    def __init__(self, bot, key, current=None):
        self.bot = bot
        self.key = key
        self.container = None
        self.listAttaker = []
        self.listDefender = []
        self.listCompleto = []
        self.firstTime = True
        self.location = None
        self.amplitud = 10
        self.enemigoX = -1
        self.enemigoY = -1
        self.energia = 0
        self.velocidad = 0

    def setLists(self):
        controllers = self.container.listController()
        for key in controllers.keys():
            if key != self.key and key[:3] == self.key[:3]:
                if key[-1] == "D":
                    controller = Services.DefenderControllerPrx.checkedCast(controllers[key])
                    self.listDefender.append(controller)
                elif key[-1] == "A":
                    controller = Services.AttackerControllerPrx.checkedCast(controllers[key])
                    self.listAttaker.append(controller)
                elif key[-1] == "C":
                    controller = Services.CompletoControllerPrx.checkedCast(controllers[key])
                    self.listCompleto.append(controller)

    def turn(self, current=None):
        print("DEFENSOR " + self.key + ": Jugador " + self.key[:3])
        sys.stdout.flush()
        self.energia = 100
        if self.firstTime:
            self.setLists()
        self.firstTime = False

        self.location = self.bot.location()
        #print(self.location)
        angulo = random.randint(0, 359)
        self.scan(angulo, self.amplitud)

        if self.energia >= 60:
            self.mover()

    def scan(self, angulo, amplitud, current = None):
        self.enemigoX = -1
        self.enemigoY = -1
        print("DEFENSOR " + self.key + ": Escaneando")
        sys.stdout.flush()

        enemigos = self.bot.scan(angulo, amplitud)

        if enemigos:
            self.enemigoX = int((self.location.x + math.cos(angulo) * random.randint(1, 5) * 100) % 1000)

            if self.enemigoX > 399:
                self.enemigoX = 399
            elif self.enemigoX < 0:
                self.enemigoX = 0

            self.enemigoY = int((self.location.y + math.sin(angulo) * random.randint(1, 5) * 100) % 1000)

            if self.enemigoY > 399:
                self.enemigoY = 399
            elif self.enemigoY < 0:
                self.enemigoY = 0

            print("DEFENSOR " + self.key + ": Enemigo detectado cerca de X=" + str(self.enemigoX) + " Y=" + str(self.enemigoY))
            print("DEFENSOR " + self.key + ": Posicion X=" + str(self.location.x) + " Y=" + str(self.location.y)+" Angulo: "+str(angulo))

    def mover(self):
        print("DEFENSOR " + self.key + ": Moviendo robot")
        sys.stdout.flush()
        if (self.velocidad == 0):
            self.bot.drive(random.randint(0, 360), 100)
            self.velocidad = 100
        elif (self.location.x > 300):
            self.bot.drive(225, 49)
            self.velocidad = 49
        elif (self.location.x < 30):
            self.bot.drive(45, 49)
            self.velocidad = 49
        elif (self.location.y > 300):
            self.bot.drive(315, 49)
            self.velocidad = 49
        elif (self.location.y < 30):
            self.bot.drive(135, 49)
            self.velocidad = 49
        self.energia -= 60

    def setContainer(self, proxy):
        self.container = Services.ContainerPrx.checkedCast(proxy)

    def posicion(self, current=None):
        pos = self.bot.location()
        print("DEFENSOR " + self.key + ": Posicion -> " + str(pos))
        return pos

    def getEnemigoX(self, current=None):
        return self.enemigoX

    def getEnemigoY(self, current=None):
        return self.enemigoY

    def robotDestroyed(self, current=None):
        print("DEFENSOR " + self.key +": Robot destruido")
        sys.stdout.flush()

class RobotControllerCompleto(Services.CompletoController):
    def __init__(self, bot, key, current=None):
        self.bot = bot
        self.key = key
        self.container = None
        self.listAttaker = []
        self.listDefender = []
        self.listCompleto = []
        self.firstTime = True
        self.location = None
        self.amplitud = 10
        self.enemigoX = -1
        self.enemigoY = -1
        self.energia = 0
        self.velocidad = 0

    def setLists(self):
        controllers = self.container.listController()
        for key in controllers.keys():
            if key != self.key and key[:3] == self.key[:3]:
                if key[-1] == "D":
                    controller = Services.DefenderControllerPrx.checkedCast(controllers[key])
                    self.listDefender.append(controller)
                elif key[-1] == "A":
                    controller = Services.AttackerControllerPrx.checkedCast(controllers[key])
                    self.listAttaker.append(controller)
                elif key[-1] == "C":
                    controller = Services.CompletoControllerPrx.checkedCast(controllers[key])
                    self.listCompleto.append(controller)

    def turn(self, current=None):
        print("COMPLETO " + self.key + ": Jugador " + self.key[:3])
        sys.stdout.flush()
        self.energia = 100
        if self.firstTime:
            self.setLists()
        self.firstTime = False

        self.location = self.bot.location()
        self.energia -= 1
        # print(self.location)
        angulo = random.randint(0, 359)
        self.scan(angulo, self.amplitud)
        self.energia -= 10

        self.shoot(1)

        if self.energia >= 60:
            self.mover()

    def scan(self, angulo, amplitud, current = None):
        self.enemigoX = -1
        self.enemigoY = -1
        print("COMPLETO " + self.key + ": Escaneando")
        sys.stdout.flush()

        enemigos = self.bot.scan(angulo, amplitud)

        if enemigos:
            self.enemigoX = int((self.location.x + math.cos(angulo) * random.randint(1, 5) * 100) % 1000)

            if self.enemigoX > 399:
                self.enemigoX = 399
            elif self.enemigoX < 0:
                self.enemigoX = 0

            self.enemigoY = int((self.location.y + math.sin(angulo) * random.randint(1, 5) * 100) % 1000)

            if self.enemigoY > 399:
                self.enemigoY = 399
            elif self.enemigoY < 0:
                self.enemigoY = 0

            print("COMPLETO " + self.key + ": Enemigo detectado cerca de X=" + str(self.enemigoX) + " Y=" + str(self.enemigoY))

    def shoot(self, cont, current=None):
        if cont > 5:
            return None
        print("COMPLETO " + self.key + ": Disparo Cancelado")
        sys.stdout.flush()
        enemigoX = self.getEnemigoX()
        enemigoY = self.getEnemigoY()

        if len(self.listDefender) > 1:
            if enemigoY < 0 or enemigoX < 0:
                enemigoX = self.getEnemigoX()
                enemigoY = self.getEnemigoY()
        if enemigoY > -1 and enemigoX > -1:
            print("enemigo X:" + str(enemigoX) + " Y:" + str(enemigoY))
            x = enemigoX - self.location.x
            y = enemigoY - self.location.y
            angulo = int(math.degrees(math.atan2(y, x)))
            if angulo < 0:
                angulo += 360
            elif angulo >= 360:
                angulo = 0

            distancia = random.randint(1, 50) * 10
            if not self.isAmigo(angulo, distancia):
                self.bot.cannon(angulo, distancia)
                self.energia -= 50
            else:
                print("COMPLETO " + self.key + ": Amigo cerca, disparo cancelado")
                sys.stdout.flush()
                self.shoot(cont + 1)


    def isAmigo(self, anguloEnemigo, distancia):
        x = self.location.x + math.cos(anguloEnemigo) * distancia
        y = self.location.y + math.sin(anguloEnemigo) * distancia
        for i in self.listDefender:
            pos = i.posicion()
            if math.fabs(pos.x - x) < 50 and math.fabs(pos.y - y) < 50:
                return True

        for i in self.listAttaker:
            pos = i.posicion()

            if math.fabs(pos.x - x) < 50 and math.fabs(pos.y - y) < 50:
                return True

        for i in self.listCompleto:
            pos = i.posicion()

            if math.fabs(pos.x - x) < 50 and math.fabs(pos.y - y) < 50:
                return True

        return False

    def mover(self):
        print("COMPLETO " + self.key + ": Moviendo robot")
        sys.stdout.flush()
        if (self.velocidad == 0):
            self.bot.drive(random.randint(0, 360), 100)
            self.velocidad = 100
        elif (self.location.x > 300):
            self.bot.drive(225, 49)
            self.velocidad = 49
        elif (self.location.x < 30):
            self.bot.drive(45, 49)
            self.velocidad = 49
        elif (self.location.y > 300):
            self.bot.drive(315, 49)
            self.velocidad = 49
        elif (self.location.y < 30):
            self.bot.drive(135, 49)
            self.velocidad = 49
        self.energia -= 60

    def setContainer(self, proxy):
        self.container = Services.ContainerPrx.checkedCast(proxy)

    def posicion(self, current=None):
        pos = self.bot.location()
        print("COMPLETO " + self.key + ": Posicion -> " + str(pos))
        return pos

    def getEnemigoX(self, current=None):
        return self.enemigoX

    def getEnemigoY(self, current=None):
        return self.enemigoY

    def robotDestroyed(self, current=None):
        print("COMPLETO " + self.key + ": Robot destruido")
        sys.stdout.flush()