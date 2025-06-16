import numpy as np
from typing import List, Tuple, Optional
from .transporte_base import ProblemaTransporteBase


class MetodoRussell(ProblemaTransporteBase):
    
    def __init__(self, costos: List[List[float]], oferta: List[float], demanda: List[float]):
        super().__init__(costos, oferta, demanda)
        self.nombre_metodo = "Metodo de Russell"
        self.descripcion_metodo = "Usa indices ui y vj basados en maximos de filas y columnas"
    
    #Resolemos utilizando el metodo
    def resolver(self) -> dict:
        self.reset_problema()
        self._paso_inicial()
        
        while self._hay_oferta_y_demanda_disponible():
            self.iteracion_actual += 1
            
            # Calcular índices ui y vj
            indices = self._calcular_indices_russell()
            
            # Calcular diferencias modificadas
            diferencias = self._calcular_diferencias_modificadas(indices)
            
            # Encontrar menor diferencia
            celda_optima = self._encontrar_menor_diferencia(diferencias)
            
            if celda_optima is None:
                break
            
            # Realizar asignación
            self._realizar_asignacion_russell(celda_optima, indices)
        
        self._finalizar_solucion()
        return self.obtener_solucion_completa()
    
    #Registramos el paso inicial
    def _paso_inicial(self) -> None:
        descripcion = (
            f"METODO DE RUSSELL - INICIO\\n\\n"
            f"Formula: cij - ui - vj\\n"
            f"ui = maximo por fila\\n"
            f"vj = maximo por columna\\n\\n"
            f"Dimensiones: {self.num_origenes}x{self.num_destinos}"
        )
        self.agregar_paso("Inicializacion Russell", descripcion)
    
    #Verificamos is hay oferta y demanda
    def _hay_oferta_y_demanda_disponible(self) -> bool:
        return np.any(self.oferta > 1e-6) and np.any(self.demanda > 1e-6)
    
    #Calculamos indices ui yv j
    def _calcular_indices_russell(self) -> dict:
        ui = []
        vj = []
        
        # ui: máximo por fila donde hay demanda
        for i in range(self.num_origenes):
            if self.oferta[i] > 1e-6:
                costos_fila = [self.costos_originales[i, j] for j in range(self.num_destinos) 
                              if self.demanda[j] > 1e-6]
                max_fila = max(costos_fila) if costos_fila else 0
                ui.append(float(max_fila))
            else:
                ui.append(0.0)
        
        # vj: máximo por columna donde hay oferta
        for j in range(self.num_destinos):
            if self.demanda[j] > 1e-6:
                costos_col = [self.costos_originales[i, j] for i in range(self.num_origenes) 
                              if self.oferta[i] > 1e-6]
                max_col = max(costos_col) if costos_col else 0
                vj.append(float(max_col))
            else:
                vj.append(0.0)
        
        return {'ui': ui, 'vj': vj}
    
    #Calculamos las diferencias
    def _calcular_diferencias_modificadas(self, indices: dict) -> np.ndarray:
        diferencias = np.full((self.num_origenes, self.num_destinos), float('inf'))
        
        for i in range(self.num_origenes):
            for j in range(self.num_destinos):
                if self.oferta[i] > 1e-6 and self.demanda[j] > 1e-6:
                    diferencias[i, j] = (self.costos_originales[i, j] - 
                                       indices['ui'][i] - indices['vj'][j])
        
        return diferencias
    #Encontramos la celda con menor diferencia
    def _encontrar_menor_diferencia(self, diferencias: np.ndarray) -> Optional[Tuple[int, int, float]]:
        min_diferencia = float('inf')
        celda_optima = None
        
        for i in range(self.num_origenes):
            for j in range(self.num_destinos):
                if (self.oferta[i] > 1e-6 and self.demanda[j] > 1e-6 and 
                    diferencias[i, j] < min_diferencia):
                    min_diferencia = diferencias[i, j]
                    celda_optima = (i, j, min_diferencia)
        
        return celda_optima
    
    #RE#alizamos la asignacion
    def _realizar_asignacion_russell(self, celda_info: Tuple[int, int, float], indices: dict) -> None:
        fila, columna, diferencia_min = celda_info
        cantidad = min(self.oferta[fila], self.demanda[columna])
        costo_unitario = self.costos_originales[fila, columna]
        
        # Asignar
        self.matriz_asignacion[fila, columna] += cantidad
        self.oferta[fila] -= cantidad
        self.demanda[columna] -= cantidad
        
        # Registrar paso
        self._registrar_paso_russell(fila, columna, cantidad, costo_unitario, 
                                    diferencia_min, indices)
    
    #REgistramos pasos
    def _registrar_paso_russell(self, fila: int, columna: int, cantidad: float,
                              costo_unitario: float, diferencia_min: float, indices: dict) -> None:
        costo_total = self.calcular_costo_actual()
        ui_celda = indices['ui'][fila]
        vj_celda = indices['vj'][columna]
        
        descripcion = (
            f"RUSSELL {self.iteracion_actual}\\n\\n"
            f"Indices: ui[{fila+1}]={ui_celda:.2f}, vj[{columna+1}]={vj_celda:.2f}\\n"
            f"Diferencia: {costo_unitario:.2f} - {ui_celda:.2f} - {vj_celda:.2f} = {diferencia_min:.2f}\\n\\n"
            f"Asignacion P{fila+1}->T{columna+1}: {cantidad:.2f} unidades\\n"
            f"Costo total: {costo_total:.2f}"
        )
        
        self.agregar_paso(f"Russell - Diferencia {diferencia_min:.2f}", descripcion,
                         celda_seleccionada=[int(fila), int(columna)], 
                         diferencia=float(diferencia_min),
                         ui=float(ui_celda), vj=float(vj_celda))
    
    #FInalizamos la solucion
    def _finalizar_solucion(self) -> None:
        self.resuelto = True
        self.costo_total_final = self.calcular_costo_actual()
        
        descripcion = (
            f"SOLUCION RUSSELL COMPLETADA\\n\\n"
            f"Costo total: {float(self.costo_total_final):.2f}\\n"
            f"Iteraciones: {self.iteracion_actual}\\n"
            f"Metodo: Indices ui/vj con diferencias modificadas"
        )
        
        self.agregar_paso("Solucion Final Russell", descripcion, solucion_final=True)
