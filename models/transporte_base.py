import numpy as np
from typing import List, Dict, Any, Tuple
import copy


class ProblemaTransporteBase:
    
    #Inicializamos la clase con los datos
    def __init__(self, costos: List[List[float]], oferta: List[float], demanda: List[float]):
        # Validar datos básicos
        if not costos or not oferta or not demanda:
            raise ValueError("Los datos de entrada no pueden estar vacíos")
        
        # Convertir a numpy arrays
        self.costos_originales = np.array(costos, dtype=float)
        self.oferta_original = np.array(oferta, dtype=float)
        self.demanda_original = np.array(demanda, dtype=float)
        
        # Dimensiones
        self.num_origenes = len(oferta)
        self.num_destinos = len(demanda)
        
        # Verificar balance
        if abs(sum(oferta) - sum(demanda)) > 1e-6:
            raise ValueError("El problema no está balanceado")
        
        # Inicializar
        self.reset_problema()
        self.nombre_metodo = "Base"
        self.descripcion_metodo = "Clase base"
    
    #Reiniciamos el problema a su estado original
    def reset_problema(self) -> None:
        self.costos = self.costos_originales.copy()
        self.oferta = self.oferta_original.copy()
        self.demanda = self.demanda_original.copy()
        self.matriz_asignacion = np.zeros((self.num_origenes, self.num_destinos))
        self.pasos_proceso = []
        self.iteracion_actual = 0
        self.resuelto = False
        self.costo_total_final = 0.0
    
    #Agregamos un paso al proeso de soluciom
    def agregar_paso(self, titulo: str, descripcion: str, **kwargs) -> None:
        # Convertir numpy arrays y números a tipos JSON-seguros
        datos_extra = {}
        for key, value in kwargs.items():
            if isinstance(value, np.ndarray):
                datos_extra[key] = value.tolist()
            elif isinstance(value, (np.integer, np.floating)):
                datos_extra[key] = float(value)
            else:
                datos_extra[key] = value
        
        paso = {
            'numero_paso': len(self.pasos_proceso) + 1,
            'titulo': str(titulo),
            'descripcion': str(descripcion),
            'iteracion': int(self.iteracion_actual),
            'matriz_asignacion': self.matriz_asignacion.copy().tolist(),
            'oferta_actual': self.oferta.copy().tolist(),
            'demanda_actual': self.demanda.copy().tolist(),
            'costo_parcial': float(self.calcular_costo_actual()),
            'metodo': str(self.nombre_metodo),
            'datos_extra': datos_extra
        }
        
        self.pasos_proceso.append(paso)
    
    #Calculamos el costo actual de la asignacion
    def calcular_costo_actual(self) -> float:
        return float(np.sum(self.matriz_asignacion * self.costos_originales))
    
    #OBtenemos la solucion completa del problema
    def obtener_solucion_completa(self) -> Dict[str, Any]:
        return {
            'metodo': str(self.nombre_metodo),
            'descripcion': str(self.descripcion_metodo),
            'matriz_solucion': self.matriz_asignacion.tolist(),
            'costo_total': float(self.calcular_costo_actual()),
            'num_pasos': len(self.pasos_proceso),
            'pasos_detallados': self.pasos_proceso,
            'problema_original': {
                'costos': self.costos_originales.tolist(),
                'oferta': self.oferta_original.tolist(),
                'demanda': self.demanda_original.tolist(),
                'dimensiones': f"{self.num_origenes}x{self.num_destinos}"
            },
            'resuelto': bool(self.resuelto)
        }
    
    #Verrificasmos si la solucion es factible
    def verificar_solucion_factible(self) -> Tuple[bool, List[str]]:
        errores = []
        
        # Verificar restricciones de oferta
        for i in range(self.num_origenes):
            suma_fila = np.sum(self.matriz_asignacion[i, :])
            oferta_original = self.oferta_original[i]
            
            if abs(suma_fila - oferta_original) > 1e-6:
                errores.append(f"Origen {i+1}: asignado {suma_fila:.2f}, disponible {oferta_original:.2f}")
        
        # Verificar restricciones de demanda
        for j in range(self.num_destinos):
            suma_columna = np.sum(self.matriz_asignacion[:, j])
            demanda_original = self.demanda_original[j]
            
            if abs(suma_columna - demanda_original) > 1e-6:
                errores.append(f"Destino {j+1}: asignado {suma_columna:.2f}, requerido {demanda_original:.2f}")
        
        return len(errores) == 0, errores
    
    #metodo a implementar en cala hijo
    def resolver(self) -> Dict[str, Any]:
        raise NotImplementedError("Este método debe ser implementado por la clase hija")
