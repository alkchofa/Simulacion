#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random


HighValue=99999
TF=240  #Tiempo para Finalizar (en minutos)
T=0     #Tiempo
TPLL=0  #Tiempo para proxima llegada
NS=0    #Numero de personas en el sistema (Cola+atendiendo)
STO=0   #Sumatoria del tiempo ocioso
ITO=0   #Intervalo del tiempo ocioso
STLL=0  #Sumatoria del tiempo de llegada
STS=0   #Sumatoria del tiempo de salida
NT=0    #Personas que pasaron por el sistema
TA=0 #Tiempo de atencion
STA=0  #Sumatoria del tiempo de atencion
PTO = 0 #Porcentaje de tiempo ocsiosos
PEC = 0 #Porcentade de espera en cola
PPS = 0 #Promedio de permanencia en el sistema
TPS = HighValue   #Tiempo para proxima salida
colaIA=[9, 11, 61, 30, 120, 20, 10]
colaTA=[13, 10, 80, 40, 20, 30, 30]


def ImprimirVariables(Evento):
    global T, NS, NT, TPLL, TPS, STLL, STS, PPS, ITO, STO, TF
    procesarSimulacion()
    print "|-Evento= "+Evento
    print "|-  T   |  NS  |  NT  | TPLL |  TPS | STLL |  STS |  PPS |  ITO |  STO |  TF "
    print "|-"+str(T).center(6," ")+"|"+str(NS).center(6," ")+"|"+str(NT).center(6," ")+"|"+str(TPLL).center(6," ")+"|"+str(TPS).center(6," ")+"|"+str(STLL).center(6," ")+"|"+str(STS).center(6," ")+"|"+str(PPS).center(6," ")+"|"+str(ITO).center(6," ")+"|"+str(STO).center(6," ")+"|"+str(TF).center(6," ")
    print "-----------------------------------------------------------------------------"
    
def DameIntervaloDeArribo():
    '''random.seed
    return random.randint(0,10)'''
    #return input("Ingrese intervalo de arribos: ")
    return colaIA.pop()

def DameTiempoAtencion():
    '''random.seed
    return random.randint(10,20)'''
    #return input("Ingrese tiempo de atencion: ")
    return colaTA.pop()

def hacerUnaLlegada():
    global T,IA,TPLL,NS,STLL,STO,TA,TPS,STA
    T=TPLL
    IA = DameIntervaloDeArribo()
    TPLL = T + IA
    NS = NS + 1
    ImprimirVariables("Llegada")
    STLL = STLL + T
    if NS == 1:
        STO = STO + (T - ITO)
        TA = DameTiempoAtencion()
        TPS = T + TA
        STA = STA + TA
    else:
        pass #hago cola

def terminarSalida():
    global STS,NT
    STS = STS + T
    NT = NT + 1

def hacerUnaSalida():
    global T,NS,TA,TPS,STA,ITO,TPS
    T = TPS
    NS = NS-1
    ImprimirVariables("Salida")
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
    if NT:
    	PPS = (STS-STLL) / NT
    	PEC = (STS-STLL-STA) / NT
    else:
    	PPS=0
    	PEC=0
    if T:
    	PTO = (STO * 100) / T
    else:
    	PTO=0

def simular():
    while T <= TF:
        hacerRutina()

#MAIN
ImprimirVariables("Empiezo")
simular()
while NS > 0:
    TPLL=HighValue
    hacerRutina()

procesarSimulacion()
ImprimirVariables("Finalizar")
print "Promedio permanencia en el sistema = " + str(PPS)
print "Promedio de espera en cola = " + str(PEC)
print "Porcentaje de tiempo ocioso = " + str(PTO)
print "Cantidad de gente que paso en el sistema = " + str(NT)
