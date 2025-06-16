from typing import List, Tuple, Dict, Any
import numpy as np


class ValidadorDatos:
    
    #validamos el problema
    @staticmethod
    def validar_problema_completo(costos: List[List[float]], 
                                 oferta: List[float], 
                                 demanda: List[float]) -> Tuple[bool, List[str]]:
        errores = []
        
        # Validaciones básicas
        if not costos or not oferta or not demanda:
            errores.append("Los datos no pueden estar vacíos")
            return False, errores
        
        # Validar dimensiones
        num_origenes = len(oferta)
        num_destinos = len(demanda)
        
        if len(costos) != num_origenes:
            errores.append(f"La matriz de costos debe tener {num_origenes} filas")
        
        # Validar valores
        for i, fila in enumerate(costos):
            if len(fila) != num_destinos:
                errores.append(f"La fila {i+1} debe tener {num_destinos} elementos")
            for j, costo in enumerate(fila):
                if costo < 0:
                    errores.append(f"El costo en P{i+1}→T{j+1} no puede ser negativo")
        
        # Validar ofertas y demandas
        for i, of in enumerate(oferta):
            if of <= 0:
                errores.append(f"La oferta del origen P{i+1} debe ser positiva")
        
        for j, dem in enumerate(demanda):
            if dem <= 0:
                errores.append(f"La demanda del destino T{j+1} debe ser positiva")
        
        # Validar balance
        total_oferta = sum(oferta)
        total_demanda = sum(demanda)
        
        if abs(total_oferta - total_demanda) > 1e-6:
            errores.append(
                f"Problema no balanceado: Oferta ({total_oferta:,.2f}) ≠ "
                f"Demanda ({total_demanda:,.2f})"
            )
        
        return len(errores) == 0, errores
    
    #Sugerimos el balancer al problema
    @staticmethod
    def sugerir_balanceo(oferta: List[float], demanda: List[float]) -> Dict[str, Any]:
        total_oferta = sum(oferta)
        total_demanda = sum(demanda)
        diferencia = total_oferta - total_demanda
        
        if abs(diferencia) < 1e-6:
            return {'balanceado': True, 'sugerencias': []}
        
        sugerencias = []
        if diferencia > 0:
            sugerencias.append(f"Agregar destino ficticio con demanda {diferencia:,.2f}")
        else:
            sugerencias.append(f"Agregar origen ficticio con oferta {abs(diferencia):,.2f}")
        
        return {
            'balanceado': False,
            'diferencia': diferencia,
            'sugerencias': sugerencias
        }
