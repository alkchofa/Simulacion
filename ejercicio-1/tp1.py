#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

class Tp1:

	def __init__(self):
		self.HighValue=99999
		self.TF=240  #Tiempo para Finalizar (en minutos)
		self.T=0     #Tiempo
		self.TPLL=0  #Tiempo para proxima llegada
		self.NS=0    #Numero de personas en el sistema (Cola+atendiendo)
		self.STO=0   #Sumatoria del tiempo ocioso
		self.ITO=0   #Intervalo del tiempo ocioso
		self.SumatoriaTiempoAtencion=0  #Sumatoria del tiempo de atencion
		self.STLL=0  #Sumatoria del tiempo de llegada
		self.STS=0   #Sumatoria del tiempo de salida
		self.NT=0    #Personas que pasaron por el sistema
		self.SumatoriaArriboCon5Personas=0
		self.SumatoriaArrepentimientos=0
		self.TPS=self.HighValue   #Tiempo para proxima salida
		self.PPS=0   #Promedio de permanencia en el sistema
		self.PromedioEsperaEnCola=0
		self.PorcentajePersonasQueSEFueronPorMasDe5PersonasEnLaFila=0
		self.Sigo = True
		self.colaIA=[9, 11, 61, 30, 120, 20, 10]
		self.colaTA=[13, 10, 80, 40, 20, 30, 30]
	
	def imprimirVariables(self,Evento):
	    print "|-Evento= "+Evento
	    print "|-  T   |  NS  |  NT  | TPLL |  TPS | STLL |  STS |  PPS |  ITO |  STO |  TF "
	    print "|-"+str(self.T).center(6," ")+"|"+str(self.NS).center(6," ")+"|"+str(self.NT).center(6," ")+"|"+str(self.TPLL).center(6," ")+"|"+str(self.TPS).center(6," ")+"|"+str(self.STLL).center(6," ")+"|"+str(self.STS).center(6," ")+"|"+str(self.PPS).center(6," ")+"|"+str(self.ITO).center(6," ")+"|"+str(self.STO).center(6," ")+"|"+str(self.TF).center(6," ")
	    print "-----------------------------------------------------------------------------"
	
	def dameIntervaloDeArribo(self):
		#return random.randint(0,10)
		#return input("Ingrese IA: ")
	    return self.colaIA.pop()
	
	def dameTiempoAtencion(self):
		#random.seed
		#return random.randint(10,20)
		#return input("Ingrese TA: ")
	    return self.colaTA.pop()
	
	def arrepentimiento(self):
		if self.NS < 5:
			return False
		else:
			if self.NS > 8:
				self.SumatoriaArrepentimientos += 1
				return True
			else:
				if random.uniform(0,1.0) <= 0.4:
					return False
				else:
					if self.NS == 6: #Esto es igual a 6, porque NS es la suma de la persona a la que atienen mas la de la cola
						self.SumatoriaArriboCon5Personas += 1
					self.SumatoriaArrepentimientos += 1
				return True
	
	def obtenerResultado(self):
		if self.NT:
			self.PPS = (self.STS-self.STLL) / self.NT
			self.PromedioEsperaEnCola = (self.STS-self.STLL-self.SumatoriaTiempoAtencion) / self.NT
		else:
			self.PPS=0
			self.PromedioEsperaEnCola=0
		if self.T:
			self.PTO = (self.STO * 100) / self.T
		else:
			self.PTO=0
		if self.SumatoriaArrepentimientos > 0:
			self.PorcentajePersonasQueSEFueronPorMasDe5PersonasEnLaFila = (self.SumatoriaArriboCon5Personas*100 / self.SumatoriaArrepentimientos)
		else:
			self.PorcentajePersonasQueSEFueronPorMasDe5PersonasEnLaFila = 0.00
		self.Sigo=False

	def procesarLlegada(self):
		self.T=self.TPLL
		self.TPLL = self.T+self.dameIntervaloDeArribo()
		if not self.arrepentimiento():
			self.NS += 1
			if self.NS == 1:
				self.STO += self.T - self.ITO
				tiempoAtencion = self.dameTiempoAtencion()
				self.TPS = self.T + tiempoAtencion
				self.SumatoriaTiempoAtencion += tiempoAtencion
			self.STLL += self.T

	def procesarSalida(self):
		self.T = self.TPS
		self.NS -= 1
		if self.NS==0:
			self.vaciamiento=False
		if self.NS >= 1:
			tiempoAtencion = self.dameTiempoAtencion()
			self.TPS = self.T + tiempoAtencion
			self.SumatoriaTiempoAtencion += tiempoAtencion
		else:
			self.TPS = self.HighValue
			self.ITO = self.T
		self.STS += self.T
		self.NT += 1

	def mostrarResultados(self):
		print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
		print "Promedio permanencia en el sistema = " + str(self.PPS)
		print "Promedio espera en cola = " + str(self.PromedioEsperaEnCola)
		print "Sumatoria tiempo ocioso= "+str(self.STO)
		print "Porcentaje de tiempo ocioso = " + "{0:.2f}".format(self.PTO)+"%"
		print "Porcentaje de personas arrepentidas con 5 personas en la cola = " + "{0:.2f}".format(self.PorcentajePersonasQueSEFueronPorMasDe5PersonasEnLaFila)+"%"
		print "Cantidad de personas que pasaron por el sistema = "+str(self.NT)
		print "Cantidad de Arrepentidos = "+str(self.SumatoriaArrepentimientos)
		print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
	
	def correrSimulacion(self):
		self.vaciamiento=False
		while self.Sigo:
			if self.T <= self.TF or self.vaciamiento:
				self.imprimirVariables("Antes de entrar")
				if self.TPLL <= self.TPS:
					self.procesarLlegada()
				else:
					self.procesarSalida()
			else:
				if self.NS >0:
					self.TPLL=self.HighValue
					self.vaciamiento=True
				else:
					self.obtenerResultado()
					self.mostrarResultados()
	
tp1 = Tp1()

tp1.imprimirVariables("Inicio")
tp1.correrSimulacion()
tp1.imprimirVariables("Fin")