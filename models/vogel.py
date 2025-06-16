import numpy as np
from typing import List, Tuple, Optional
from .transporte_base import ProblemaTransporteBase


class MetodoVogel(ProblemaTransporteBase):
    
    def __init__(self, costos: List[List[float]], oferta: List[float], demanda: List[float]):
        super().__init__(costos, oferta, demanda)
        self.nombre_metodo = "Metodo de Vogel (VAM)"
        self.descripcion_metodo = "Usa penalizaciones basadas en diferencias de costos"
    
    #Resolvemos con el metodo seleccionado
    def resolver(self) -> dict:
        self.reset_problema()
        self._paso_inicial()
        
        while self._hay_oferta_y_demanda_disponible():
            self.iteracion_actual += 1
            
            # Calcular penalizaciones
            penalizaciones = self._calcular_penalizaciones()
            
            # Encontrar la mayor penalización
            seleccion = self._encontrar_mayor_penalizacion(penalizaciones)
            
            if seleccion is None:
                break
            
            # Realizar asignación
            self._realizar_asignacion_vogel(seleccion, penalizaciones)
        
        self._finalizar_solucion()
        return self.obtener_solucion_completa()
    
    #Registrar el paso inicial del metodo
    def _paso_inicial(self) -> None:
        descripcion = (
            f"METODO DE VOGEL (VAM) - INICIO\\n\\n"
            f"Estrategia: Calcularemos penalizaciones por fila y columna "
            f"basadas en la diferencia entre los dos menores costos.\\n\\n"
            f"Dimensiones: {self.num_origenes}x{self.num_destinos}"
        )
        
        self.agregar_paso("Inicializacion VAM", descripcion)
    
    #Verificamos si hay oferta y demanda disponible
    def _hay_oferta_y_demanda_disponible(self) -> bool:
        return np.any(self.oferta > 1e-6) and np.any(self.demanda > 1e-6)
    
    #Calculamos las penalizaciones por fila y columna
    def _calcular_penalizaciones(self) -> dict:
        penalizaciones_fila = []
        penalizaciones_columna = []
        
        # Penalizaciones por fila
        for i in range(self.num_origenes):
            if self.oferta[i] > 1e-6:
                costos_disponibles = []
                for j in range(self.num_destinos):
                    if self.demanda[j] > 1e-6:
                        costos_disponibles.append(self.costos_originales[i, j])
                
                if len(costos_disponibles) >= 2:
                    costos_disponibles.sort()
                    penalizacion = costos_disponibles[1] - costos_disponibles[0]
                elif len(costos_disponibles) == 1:
                    penalizacion = 0
                else:
                    penalizacion = -1
                
                penalizaciones_fila.append(float(penalizacion))
            else:
                penalizaciones_fila.append(-1.0)
        
        # Penalizaciones por columna
        for j in range(self.num_destinos):
            if self.demanda[j] > 1e-6:
                costos_disponibles = []
                for i in range(self.num_origenes):
                    if self.oferta[i] > 1e-6:
                        costos_disponibles.append(self.costos_originales[i, j])
                
                if len(costos_disponibles) >= 2:
                    costos_disponibles.sort()
                    penalizacion = costos_disponibles[1] - costos_disponibles[0]
                elif len(costos_disponibles) == 1:
                    penalizacion = 0
                else:
                    penalizacion = -1
                
                penalizaciones_columna.append(float(penalizacion))
            else:
                penalizaciones_columna.append(-1.0)
        
        return {'filas': penalizaciones_fila, 'columnas': penalizaciones_columna}
    
    #Encontramos la fila o columna con mayor penalizacion
    def _encontrar_mayor_penalizacion(self, penalizaciones: dict) -> Optional[dict]:
        max_penalizacion = -1
        seleccion = None
        
        # Revisar penalizaciones de filas
        for i, pen in enumerate(penalizaciones['filas']):
            if pen > max_penalizacion and pen != -1:
                max_penalizacion = pen
                seleccion = {'tipo': 'fila', 'indice': i, 'penalizacion': pen}
        
        # Revisar penalizaciones de columnas
        for j, pen in enumerate(penalizaciones['columnas']):
            if pen > max_penalizacion and pen != -1:
                max_penalizacion = pen
                seleccion = {'tipo': 'columna', 'indice': j, 'penalizacion': pen}
        
        return seleccion
    
    #Realizamos la asignacion a fila o columna
    def _realizar_asignacion_vogel(self, seleccion: dict, penalizaciones: dict) -> None:
        if seleccion['tipo'] == 'fila':
            celda_optima = self._encontrar_menor_costo_en_fila(seleccion['indice'])
        else:
            celda_optima = self._encontrar_menor_costo_en_columna(seleccion['indice'])
        
        if celda_optima is None:
            return
        
        i, j, costo_unitario = celda_optima
        cantidad = min(self.oferta[i], self.demanda[j])
        
        # Realizar asignación
        self.matriz_asignacion[i, j] += cantidad
        self.oferta[i] -= cantidad
        self.demanda[j] -= cantidad
        
        # Registrar el paso
        self._registrar_paso_vogel(i, j, cantidad, costo_unitario, seleccion)
    
    #Encontramos el menor costo en la fila
    def _encontrar_menor_costo_en_fila(self, fila: int) -> Optional[Tuple[int, int, float]]:
        menor_costo = float('inf')
        celda_optima = None
        
        for j in range(self.num_destinos):
            if self.demanda[j] > 1e-6:
                costo = self.costos_originales[fila, j]
                if costo < menor_costo:
                    menor_costo = costo
                    celda_optima = (fila, j, costo)
        
        return celda_optima
    
    #Encontramos el menor costo en la columna
    def _encontrar_menor_costo_en_columna(self, columna: int) -> Optional[Tuple[int, int, float]]:
        menor_costo = float('inf')
        celda_optima = None
        
        for i in range(self.num_origenes):
            if self.oferta[i] > 1e-6:
                costo = self.costos_originales[i, columna]
                if costo < menor_costo:
                    menor_costo = costo
                    celda_optima = (i, columna, costo)
        
        return celda_optima
    
    #registramos el paso
    def _registrar_paso_vogel(self, fila: int, columna: int, cantidad: float,
                             costo_unitario: float, seleccion: dict) -> None:
        costo_celda = cantidad * costo_unitario
        costo_total = self.calcular_costo_actual()
        
        descripcion = (
            f"ITERACION VAM {self.iteracion_actual}\\n\\n"
            f"Mayor penalizacion: {float(seleccion['penalizacion']):.2f} en "
            f"{seleccion['tipo']} {seleccion['indice'] + 1}\\n\\n"
            f"Asignacion P{fila+1}->T{columna+1}: {float(cantidad):.2f} unidades\\n"
            f"Costo unitario: {float(costo_unitario):.2f}\\n"
            f"Costo total: {float(costo_total):.2f}"
        )
        
        self.agregar_paso(f"VAM - Penalizacion {float(seleccion['penalizacion']):.2f}", 
                         descripcion,
                         celda_seleccionada=[int(fila), int(columna)],
                         cantidad_asignada=float(cantidad),
                         costo_unitario=float(costo_unitario))
    
    #FInalizamos solucion
    def _finalizar_solucion(self) -> None:
        self.resuelto = True
        self.costo_total_final = self.calcular_costo_actual()
        
        descripcion = (
            f"SOLUCION COMPLETADA - METODO VAM\\n\\n"
            f"Costo total: {float(self.costo_total_final):.2f}\\n"
            f"Iteraciones: {self.iteracion_actual}\\n"
            f"VAM ofrece un buen compromiso entre calidad y eficiencia."
        )
        
        self.agregar_paso("Solucion Final VAM", descripcion, solucion_final=True)
