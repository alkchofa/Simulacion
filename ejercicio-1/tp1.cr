#!/usr/bin/crystal

class Tp1

	def initialize()
		@HighValue=99999
		@TF=240  #Tiempo para Finalizar (en minutos)
		@T=0     #Tiempo
		@TPLL=0  #Tiempo para proxima llegada
		@NS=0    #Numero de personas en el sistema (Cola+atendiendo)
		@STO=0   #Sumatoria del tiempo ocioso
		@ITO=0   #Intervalo del tiempo ocioso
		@SumatoriaTiempoAtencion=0  #Sumatoria del tiempo de atencion
		@STLL=0  #Sumatoria del tiempo de llegada
		@STS=0   #Sumatoria del tiempo de salida
		@NT=0    #Personas que pasaron por el sistema
		@SumatoriaArriboCon5Personas=0
		@SumatoriaArrepentimientos=0
		@TPS=@HighValue   #Tiempo para proxima salida
		@PPS=0   #Promedio de permanencia en el sistema
		@PromedioEsperaEnCola=0
		@PorcentajePersonasQueSEFueronPorMasDe5PersonasEnLaFila=0
		@Sigo = true
		@colaIA=[9, 11, 61, 30, 120, 20, 10]
		@colaTA=[13, 10, 80, 40, 20, 30, 30]
	end

	private def center(cadena, cantidad, caracter)
		ladoDer=(cantidad-cadena.size)/2
		ladoIzq=cantidad-ladoDer-cadena.size
		cadena=cadena.ljust(cadena.size+ladoDer,caracter)
		cadena=cadena.rjust(cadena.size+ladoIzq,caracter)
		return cadena
	end

	def imprimirVariables(evento)
		puts "|-Evento= #{evento}"
	    puts "|-   T  |  NS  |  NT  | TPLL |  TPS | STLL |  STS |  PPS |  ITO |  STO |  TF "
	    puts "|-"+center(@T.to_s,6,' ')+"|"+center(@NS.to_s,6,' ')+"|"+center(@NT.to_s,6,' ')+"|"+center(@TPLL.to_s,6,' ')+"|"+center(@TPS.to_s,6,' ')+"|"+center(@STLL.to_s,6,' ')+"|"+center(@STS.to_s,6,' ')+"|"+center(@PPS.to_s,6,' ')+"|"+center(@ITO.to_s,6,' ')+"|"+center(@STO.to_s,6,' ')+"|"+center(@TF.to_s,6,' ')
	    puts "-----------------------------------------------------------------------------"
	end

	def dameIntervaloDeArribo
		#return random.randint(0,10)
		#return input("Ingrese IA: ")
	    return @colaIA.pop
	end

	def dameTiempoAtencion
		#random.seed
		#return random.randint(10,20)
		#return input("Ingrese TA: ")
	    return @colaTA.pop
	end
		
	def arrepentimiento
	    if @NS < 5
	        return false
	    else
	        if @NS > 8
	            @SumatoriaArrepentimientos += 1
	            return true
	        else
	            if rand <= 0.4
	                return false
	            else
	            	if @NS == 6 #Esto es igual a 6, porque NS es la suma de la persona a la que atienen mas la de la cola
	            		@SumatoriaArriboCon5Personas += 1
	            	end
	                @SumatoriaArrepentimientos += 1
	                return true
	            end
	        end
	    end
    end

    def obtenerResultado
	    if @NT
	        @PPS = (@STS-@STLL) / @NT
	        @PromedioEsperaEnCola = (@STS-@STLL-@SumatoriaTiempoAtencion) / @NT
	    else
	        @PPS=0
	        @PromedioEsperaEnCola=0
	    end
	    if @T
	        @PTO = (@STO * 100) / @T
	    else
	        @PTO=0
	    end
	    if @SumatoriaArrepentimientos > 0
	        @PorcentajePersonasQueSEFueronPorMasDe5PersonasEnLaFila = (@SumatoriaArriboCon5Personas*100 / @SumatoriaArrepentimientos)
	    else
	        @PorcentajePersonasQueSEFueronPorMasDe5PersonasEnLaFila = 0.00
	    end
	    @Sigo=false
	end

	def procesarLlegada
		@T=@TPLL
        @TPLL = @T+dameIntervaloDeArribo
        unless arrepentimiento
        	@NS += 1
            if @NS == 1
                @STO += @T - @ITO
                tiempoAtencion = dameTiempoAtencion
                @TPS = @T + tiempoAtencion
                @SumatoriaTiempoAtencion += tiempoAtencion
            end
            @STLL += @T
        end
	end

	def procesarSalida
		@T = @TPS
        @NS -= 1
        if @NS==0
          	@vaciamiento=false
        end
        if @NS >= 1
            tiempoAtencion = dameTiempoAtencion
            @TPS = @T + tiempoAtencion
            @SumatoriaTiempoAtencion += tiempoAtencion
        else
            @TPS = @HighValue
            @ITO = @T
        end
        @STS += @T
        @NT += 1
	end

	def mostrarResultados
		puts "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
		puts "Promedio permanencia en el sistema = " + @PPS.to_s
		puts "Promedio espera en cola = " + @PromedioEsperaEnCola.to_s
		puts "Sumatoria tiempo ocioso= "+@STO.to_s
		puts "Porcentaje de tiempo ocioso = " + @PTO.to_s+"%"
		puts "Porcentaje de personas arrepentidas con 5 personas en la cola = " +@PorcentajePersonasQueSEFueronPorMasDe5PersonasEnLaFila.to_s+"%"
		puts "Cantidad de personas que pasaron por el sistema = "+@NT.to_s
		puts "Cantidad de Arrepentidos = "+@SumatoriaArrepentimientos.to_s
		puts "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
	end

	def correrSimulacion
		@vaciamiento=false
		while @Sigo
			if @T <= @TF || @vaciamiento
				imprimirVariables("Antes de entrar")
				if @TPLL <= @TPS
					procesarLlegada
				else
					procesarSalida
				end
			else
				if @NS >0
					@TPLL=@HighValue
					@vaciamiento=true
				else
					obtenerResultado
					mostrarResultados
				end
			end
		end
	end	
end




tp1 = Tp1.new

tp1.imprimirVariables("Inicio")
tp1.correrSimulacion
tp1.imprimirVariables("Fin")
