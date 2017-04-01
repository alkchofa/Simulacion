#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random


HighValue=999999999
TF=240  #Tiempo para Finalizar (en minutos)
T=0     #Tiempo
TPLL=0  #Tiempo para proxima llegada
NS=0    #Numero de personas en el sistema (Cola+atendiendo)
STO=0   #Sumatoria del tiempo ocioso
ITO=0   #Intervalo del tiempo ocioso
SLL=0  #Sumatoria del tioempo de llegada
SS=0   #Sumatoria del tiempo de salida
NT=0    #Personas que pasaron por el sistema
TA=0 #Tiempo de atencion
STA=0  #Sumatoria del tiempo de atencion
PTO = 0 #Porcentaje de tiempo ocsiosos
PEC = 0 #Porcentade de espera en cola
PPS = 0 #Promedio de permanencia en el sistema
TPS = HighValue   #Tiempo para proxima salida

def DameIntervaloDeArribo():
    '''random.seed
    return random.randint(0,10)'''
    return input("Ingrese intervalo de arribos: ")

def DameTiempoAtencion():
    '''random.seed
    return random.randint(10,20)'''
    return input("Ingrese tiempo de atencion: ")

def hacerUnaLlegada():
    global T,IA,TPLL,NS,SLL,STO,TA,TPS,STA
    T=TPLL
    IA = DameIntervaloDeArribo()
    TPLL = T + IA
    NS = NS + 1
    SLL = SLL + T
    if NS == 1:
        STO = STO + (T - ITO)
        TA = DameTiempoAtencion()
        TPS = T + TA
        STA = STA + TA
    else:
        pass #hago cola

def terminarSalida():
    global SS,NT
    SS = SS + T
    NT = NT + 1

def hacerUnaSalida():
    global T,NS,TA,TPS,STA,ITO,TPS
    T = TPS
    NS = NS-1
    if NS >= 1:
        TA = DameTiempoAtencion()
        TPS = T + TA
        STA = STA + TA
        terminarSalida()
    else:
        ITO=T
        TPS=HighValue
        terminarSalida()

def hacerRutina():
    if TPLL <= TPS:
        hacerUnaLlegada()
    else:
        hacerUnaSalida()


def procesarSimulacion():
    global PPS,PEC,PTO
    PPS = (SS-SLL) / NT
    PEC = (SS-SLL-STA) / NT
    PTO = (STO * 100) / T


def simular():
    while T <= TF:
        hacerRutina()

#MAIN
simular()
while NS > 0:
    TPLL=HighValue
    hacerRutina()


procesarSimulacion()
print "Promedio permanencia en el sistema = " + str(PPS)
print "Promedio de espera en cola = " + str(PEC)
print "Porcentaje de tiempo ocioso = " + str(PTO)
print "Cantidad de gente que paso en el sistema = " + str(NT)
