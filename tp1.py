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
SumatoriaTiempoAtencion=0  #Sumatoria del tiempo de atencion
STLL=0  #Sumatoria del tioempo de llegada
STS=0   #Sumatoria del tiempo de salida
NT=0    #Personas que pasaron por el sistema
SumatoriaArriboCon5Personas=0
SumatoriaArrepentimientos=0
TPS=HighValue   #Tiempo para proxima salida
Sigo = True

def DameIntervaloDeArribo():
    '''random.seed
    return random.randint(0,10)'''
    return input("Ingrese IA: ")

def DameTiempoAtencion():
    '''random.seed
    return random.randint(10,20)'''
    return input("Ingrese TA: ")

def Arrepentimiento(NS):
    random.seed()
    global SumatoriaArrepentimientos
    global SumatoriaArriboCon5Personas
    if NS < 5:
        return False
    else:
        if NS > 8:
            SumatoriaArrepentimientos = SumatoriaArrepentimientos + 1
            return True
        else:
            ValorRandom = random.uniform(0,1.0)
            if ValorRandom <= 0.4:
                return False
            else:
            	if NS == 6: #Esto es igual a 6, porque NS es la suma de la persona a la que atienen mas la de la cola
            		SumatoriaArriboCon5Personas = SumatoriaArriboCon5Personas + 1
                SumatoriaArrepentimientos = SumatoriaArrepentimientos + 1
                return True

Vaciamiento=False
while Sigo:
    if T <= TF or Vaciamiento:
        if TPLL <= TPS:
            T=TPLL
            IntervaloArribo = DameIntervaloDeArribo() #Aca deberia generar el intervalo segun la tabla
            TPLL = T+IntervaloArribo
            if not Arrepentimiento(NS):
                NS = NS + 1
                if NS == 1:
                    STO = STO + (T - ITO)
                    TiempoAtencion = DameTiempoAtencion() #Aca deberia generar el intervalo segun la tabla
                    TPS = T + TiempoAtencion
                    SumatoriaTiempoAtencion = SumatoriaTiempoAtencion + TiempoAtencion
                STLL = STLL + T
        else:
            T = TPS
            NS = NS - 1
            if NS==0:
            	Vaciamiento=False
            if NS >= 1:
                TiempoAtencion = DameTiempoAtencion()
                TPS = T + TiempoAtencion
                SumatoriaTiempoAtencion = SumatoriaTiempoAtencion + TiempoAtencion
            else:
                TPS = HighValue
                ITO = T
            STS = STS + T
            NT = NT + 1
    else:
	    if NS > 0:
	        TPLL = HighValue
	        Vaciamiento=True
	    else:
	        PPS = (STS - STLL) / NT
	        PromedioEsperaEnCola = (STS - STLL - SumatoriaTiempoAtencion) / NT
	        PTO = (STO * 100) / T
	        if SumatoriaArrepentimientos > 0:
	            PorcentajePersonasQueSEFueronPorMasDe5PersonasEnLaFila = (SumatoriaArriboCon5Personas*100 / float(SumatoriaArrepentimientos))
	        else:
	            PorcentajePersonasQueSEFueronPorMasDe5PersonasEnLaFila = 0.00
	        Sigo = False

print "Promedio permanencia en el sistema = " + str(PPS)
print "Promedio espera en cola = " + str(PromedioEsperaEnCola)
print "Porcentaje de tiempo ocioso = " + str(PTO)+"%"
print "Porcentaje de personas arrepentidas con 5 personas en la cola = " + "{0:.2f}".format(PorcentajePersonasQueSEFueronPorMasDe5PersonasEnLaFila)+"%"
print "Cantidad de personas que pasaron por el sistema = "+str(NT)
print "Cantidad de Arrepentidos = "+str(SumatoriaArrepentimientos)
