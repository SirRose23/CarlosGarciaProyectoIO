import numpy as np
from typing import List, Tuple, Optional
from .transporte_base import ProblemaTransporteBase


class MetodoCostoMinimo(ProblemaTransporteBase):
    
    def __init__(self, costos: List[List[float]], oferta: List[float], demanda: List[float]):
        super().__init__(costos, oferta, demanda)
        self.nombre_metodo = "Costo Minimo"
        self.descripcion_metodo = "Asigna siempre al costo unitario mas bajo disponible"
    
    # MEtodo para llamar la funcion desdde el endpoint
    def resolver(self) -> dict:
        self.reset_problema()
        self._paso_inicial()
        
        while self._hay_oferta_y_demanda_disponible():
            self.iteracion_actual += 1
            celda_minima = self._encontrar_celda_costo_minimo()
            
            if celda_minima is None:
                break
            
            self._realizar_asignacion(celda_minima)
        
        self._finalizar_solucion()
        return self.obtener_solucion_completa()
    
    def _paso_inicial(self) -> None:
        descripcion = (
            f"METODO DE COSTO MINIMO - INICIO\\n\\n"
            f"Estrategia: Buscaremos la celda con el menor costo "
            f"unitario disponible y asignaremos la maxima cantidad posible.\\n\\n"
            f"Estado inicial:\\n"
            f"Origenes: {self.num_origenes}\\n"
            f"Destinos: {self.num_destinos}\\n"
            f"Oferta total: {float(np.sum(self.oferta)):.2f}\\n"
            f"Demanda total: {float(np.sum(self.demanda)):.2f}"
        )
        
        self.agregar_paso(
            titulo="Inicializacion del Metodo",
            descripcion=descripcion,
            matriz_costos=self.costos_originales.tolist()
        )
    
    # Verificamos si hay oferta y demanda disponibles
    def _hay_oferta_y_demanda_disponible(self) -> bool:
        return np.any(self.oferta > 1e-6) and np.any(self.demanda > 1e-6)   
    
    #Encontramos la celda con el costo minimo
    def _encontrar_celda_costo_minimo(self) -> Optional[Tuple[int, int, float]]:
        costo_minimo = float('inf')
        celda_optima = None
        
        for i in range(self.num_origenes):
            for j in range(self.num_destinos):
                if self.oferta[i] > 1e-6 and self.demanda[j] > 1e-6:
                    costo_actual = self.costos_originales[i, j]
                    if costo_actual < costo_minimo:
                        costo_minimo = costo_actual
                        celda_optima = (i, j, costo_actual)
        
        return celda_optima
    
    #Realizamos la asiganacion 
    def _realizar_asignacion(self, celda_info: Tuple[int, int, float]) -> None:
        fila, columna, costo_unitario = celda_info
        cantidad_maxima = min(self.oferta[fila], self.demanda[columna])
        
        # Realizar asignación
        self.matriz_asignacion[fila, columna] += cantidad_maxima
        self.oferta[fila] -= cantidad_maxima
        self.demanda[columna] -= cantidad_maxima
        
        # Registrar paso
        self._registrar_paso_asignacion(fila, columna, costo_unitario, cantidad_maxima)
    
    #Registramos el paso de la asignacion
    def _registrar_paso_asignacion(self, fila: int, columna: int, 
                                  costo_unitario: float, cantidad: float) -> None:
        costo_celda = cantidad * costo_unitario
        costo_total = self.calcular_costo_actual()
        
        descripcion = (
            f"ASIGNACION {self.iteracion_actual}\\n\\n"
            f"Celda seleccionada: P{fila+1} -> T{columna+1}\\n"
            f"Costo unitario: {float(costo_unitario):.2f}\\n"
            f"Cantidad asignada: {float(cantidad):.2f} unidades\\n"
            f"Costo de esta asignacion: {float(costo_celda):.2f}\\n"
            f"Costo total acumulado: {float(costo_total):.2f}"
        )
        
        self.agregar_paso(
            titulo=f"Asignacion a Costo Minimo",
            descripcion=descripcion,
            celda_seleccionada=[int(fila), int(columna)],
            costo_unitario=float(costo_unitario),
            cantidad_asignada=float(cantidad),
            costo_celda=float(costo_celda)
        )
    
    #Finalizamos la solucion y registro
    def _finalizar_solucion(self) -> None:
        self.resuelto = True
        self.costo_total_final = self.calcular_costo_actual()
        
        descripcion = (
            f"SOLUCION COMPLETADA - METODO DE COSTO MINIMO\\n\\n"
            f"Costo total optimo: {float(self.costo_total_final):.2f}\\n"
            f"Numero de iteraciones: {self.iteracion_actual}\\n"
            f"El metodo de costo minimo ha encontrado una solucion "
            f"que prioriza la eficiencia economica."
        )
        
        self.agregar_paso(
            titulo="Solucion Final Alcanzada",
            descripcion=descripcion,
            solucion_final=True,
            costo_final=float(self.costo_total_final)
        )
