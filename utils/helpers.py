import json
from typing import Any, Dict, List
from datetime import datetime


def formatear_numero(numero: float, decimales: int = 2) -> str:
    #Formateamos un numero 
    return f"{numero:,.{decimales}f}"


def formatear_moneda(cantidad: float) -> str:
    #FOrmateamos una moneda
    return f"${cantidad:,.2f}"


def generar_timestamp() -> str:
   #Timestaps
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def exportar_json(datos: Dict[str, Any], nombre_archivo: str) -> bool:
    #Exportamos a json
    try:
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False


def crear_resumen_comparativo(resultados: Dict[str, Any]) -> Dict[str, Any]:
    #REsumen comparativo de los metodos
    if not resultados:
        return {"error": "No hay resultados para comparar"}
    
    costos = {}
    estadisticas = {}
    
    for metodo, resultado in resultados.items():
        if 'costo_total' in resultado:
            costos[metodo] = resultado['costo_total']
            estadisticas[metodo] = {
                'costo': resultado['costo_total'],
                'pasos': len(resultado.get('pasos_detallados', [])),
                'asignaciones': sum(sum(fila) > 0 for fila in resultado.get('matriz_solucion', []))
            }
    
    if not costos:
        return {"error": "No se encontraron costos válidos"}
    
    # Encontrar el mejor método
    mejor_metodo = min(costos.keys(), key=lambda k: costos[k])
    mejor_costo = costos[mejor_metodo]
    
    # Calcular diferencias
    comparacion = {}
    for metodo, costo in costos.items():
        diferencia = costo - mejor_costo
        porcentaje = (diferencia / mejor_costo * 100) if mejor_costo > 0 else 0
        
        comparacion[metodo] = {
            'costo_total': costo,
            'diferencia_absoluta': diferencia,
            'diferencia_porcentual': porcentaje,
            'es_optimo': metodo == mejor_metodo,
            'estadisticas': estadisticas.get(metodo, {})
        }
    
    return {
        'mejor_metodo': mejor_metodo,
        'mejor_costo': mejor_costo,
        'comparacion': comparacion,
        'num_metodos_comparados': len(costos)
    }


def validar_entrada_numerica(valor: str, tipo: str = "float") -> tuple:
    #validamos entrada numerica
    try:
        if tipo == "int":
            valor_convertido = int(valor)
            return True, valor_convertido, ""
        else:
            valor_convertido = float(valor)
            return True, valor_convertido, ""
    except ValueError:
        return False, None, f"'{valor}' no es un {tipo} válido"


def generar_matriz_ejemplo(filas: int, columnas: int, tipo: str = "simple") -> Dict[str, List]:
    #La matriz de pureba
    import random
    
    if tipo == "simple":
        # Ejemplo simple con números pequeños
        costos = [[i + j + 1 for j in range(columnas)] for i in range(filas)]
        oferta = [10 * (i + 1) for i in range(filas)]
        demanda = [sum(oferta) // columnas] * columnas
        
        # Ajustar última demanda para balance exacto
        demanda[-1] = sum(oferta) - sum(demanda[:-1])
        
    elif tipo == "complejo":
        # Ejemplo más complejo con variación
        base_costos = [
            [500, 750, 300, 450],
            [650, 800, 400, 600],
            [400, 700, 500, 550],
            [200, 100, 400, 300]
        ]
        
        costos = base_costos[:filas]
        for fila in costos:
            while len(fila) < columnas:
                fila.append(random.randint(100, 800))
            fila[:] = fila[:columnas]
        
        oferta = [12, 17, 11, 10][:filas]
        demanda = [20, 10, 10, 10][:columnas]
        
        # Balancear
        total_oferta = sum(oferta)
        total_demanda = sum(demanda)
        if total_oferta != total_demanda:
            demanda[-1] += total_oferta - total_demanda
    
    else:  # aleatorio
        random.seed(42)  # Para reproducibilidad
        costos = [[random.randint(100, 1000) for _ in range(columnas)] for _ in range(filas)]
        oferta = [random.randint(10, 50) for _ in range(filas)]
        
        total_oferta = sum(oferta)
        demanda = [total_oferta // columnas] * columnas
        demanda[-1] += total_oferta % columnas
    
    return {
        'costos': costos,
        'oferta': oferta,
        'demanda': demanda
    }


def calcular_estadisticas_metodo(pasos: List[Dict]) -> Dict[str, Any]:
   #Estadisticas del metodo
    if not pasos:
        return {"error": "No hay pasos para analizar"}
    
    # Extraer costos de cada paso
    costos_por_paso = []
    for paso in pasos:
        if 'costo_parcial' in paso:
            costos_por_paso.append(paso['costo_parcial'])
    
    # Calcular estadísticas
    estadisticas = {
        'total_pasos': len(pasos),
        'costo_inicial': costos_por_paso[0] if costos_por_paso else 0,
        'costo_final': costos_por_paso[-1] if costos_por_paso else 0,
        'incremento_promedio': 0,
        'pasos_con_asignacion': 0
    }
    
    # Contar pasos con asignación
    for paso in pasos:
        if paso.get('datos_extra', {}).get('cantidad_asignada', 0) > 0:
            estadisticas['pasos_con_asignacion'] += 1
    
    # Calcular incremento promedio
    if len(costos_por_paso) > 1:
        incrementos = [costos_por_paso[i] - costos_por_paso[i-1] 
                      for i in range(1, len(costos_por_paso))]
        estadisticas['incremento_promedio'] = sum(incrementos) / len(incrementos)
    
    return estadisticas
