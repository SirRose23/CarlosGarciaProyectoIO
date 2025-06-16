import numpy as np
from typing import List
from .transporte_base import ProblemaTransporteBase


class MetodoEsquinaNoroeste(ProblemaTransporteBase):
    
    def __init__(self, costos: List[List[float]], oferta: List[float], demanda: List[float]):
        super().__init__(costos, oferta, demanda)
        self.nombre_metodo = "Esquina Noroeste"
        self.descripcion_metodo = "Avanza sistematicamente desde la esquina superior izquierda"
        self.fila_actual = 0
        self.columna_actual = 0
    #Resolvemos utilizando el metodo
    def resolver(self) -> dict:
        self.reset_problema()
        self.fila_actual = 0
        self.columna_actual = 0
        
        self._paso_inicial()
        
        while self._dentro_de_limites():
            self.iteracion_actual += 1
            self._realizar_asignacion_actual()
            self._mover_siguiente_posicion()
        
        self._finalizar_solucion()
        return self.obtener_solucion_completa()
    
    #Registramos el paso inicial
    def _paso_inicial(self) -> None:
        descripcion = (
            f"METODO DE ESQUINA NOROESTE - INICIO\\n\\n"
            f"Comenzamos en P{self.fila_actual + 1}, T{self.columna_actual + 1} "
            f"y avanzamos sistematicamente.\\n\\n"
            f"Dimensiones: {self.num_origenes}x{self.num_destinos}\\n"
            f"Oferta total: {float(np.sum(self.oferta)):.2f}\\n"
            f"Demanda total: {float(np.sum(self.demanda)):.2f}"
        )
        self.agregar_paso("Inicializacion", descripcion)
    
    #VErificamos si esteamos dentor de los limintes
    def _dentro_de_limites(self) -> bool:
        return (self.fila_actual < self.num_origenes and 
                self.columna_actual < self.num_destinos and
                (np.any(self.oferta > 1e-6) or np.any(self.demanda > 1e-6)))
    
    #Asigamos la cantidad actual
    def _realizar_asignacion_actual(self) -> None:
        i, j = self.fila_actual, self.columna_actual
        
        if self.oferta[i] <= 1e-6 or self.demanda[j] <= 1e-6:
            return
        
        cantidad = min(self.oferta[i], self.demanda[j])
        costo = self.costos_originales[i, j]
        
        self.matriz_asignacion[i, j] = cantidad
        self.oferta[i] -= cantidad
        self.demanda[j] -= cantidad
        
        descripcion = (
            f"ASIGNACION {self.iteracion_actual}\\n"
            f"P{i+1} -> T{j+1}: {float(cantidad):.2f} unidades\\n"
            f"Costo unitario: {float(costo):.2f}\\n"
            f"Costo total: {float(self.calcular_costo_actual()):.2f}"
        )
        
        self.agregar_paso(f"Asignacion P{i+1}->T{j+1}", descripcion,
                         celda_actual=[int(i), int(j)], 
                         quantidade=float(cantidad), 
                         costo_unitario=float(costo))
    
    #Movemos a la siguiente posicion
    def _mover_siguiente_posicion(self) -> None:
        oferta_agotada = abs(self.oferta[self.fila_actual]) < 1e-6
        demanda_satisfecha = abs(self.demanda[self.columna_actual]) < 1e-6
        
        if oferta_agotada and demanda_satisfecha:
            self.fila_actual += 1
            self.columna_actual += 1
        elif oferta_agotada:
            self.fila_actual += 1
        elif demanda_satisfecha:
            self.columna_actual += 1
    
    #Finalizamos la solucion
    def _finalizar_solucion(self) -> None:
        self.resuelto = True
        self.costo_total_final = self.calcular_costo_actual()
        
        descripcion = (
            f"SOLUCION COMPLETADA\\n\\n"
            f"Costo total: {float(self.costo_total_final):.2f}\\n"
            f"Iteraciones: {self.iteracion_actual}\\n"
            f"Metodo: Sistematico y rapido"
        )
        
        self.agregar_paso("Solucion Final", descripcion, solucion_final=True)
