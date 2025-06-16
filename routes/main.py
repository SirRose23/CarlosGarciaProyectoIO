from flask import Blueprint, render_template, request, jsonify
from models import (ProblemaTransporteBase, MetodoCostoMinimo, 
                   MetodoEsquinaNoroeste, MetodoVogel, MetodoRussell)
from utils import ValidadorDatos, crear_resumen_comparativo

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('index.html')

#Validamos datos del problema
@main_bp.route('/validar', methods=['POST'])
def validar_datos():
    try:
        datos = request.json
        costos = datos.get('costos', [])
        oferta = datos.get('oferta', [])
        demanda = datos.get('demanda', [])
        
        # Validar datos
        es_valido, errores = ValidadorDatos.validar_problema_completo(costos, oferta, demanda)
        
        response = {
            'valido': es_valido,
            'errores': errores,
            'oferta_total': sum(oferta) if oferta else 0,
            'demanda_total': sum(demanda) if demanda else 0
        }
        
        # Agregar sugerencias si no está balanceado
        if not es_valido and oferta and demanda:
            sugerencias = ValidadorDatos.sugerir_balanceo(oferta, demanda)
            response['sugerencias'] = sugerencias
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'valido': False,
            'errores': [f'Error en validación: {str(e)}']
        }), 400

#Enpinto para resolver problemas de transporte
@main_bp.route('/resolver', methods=['POST'])
def resolver_problema():
    try:
        datos = request.json
        
        # Extraer datos del problema
        costos = datos.get('costos', [])
        oferta = datos.get('oferta', [])
        demanda = datos.get('demanda', [])
        metodos_seleccionados = datos.get('metodos', ['costo_minimo'])
        
        # Validar datos antes de resolver
        es_valido, errores = ValidadorDatos.validar_problema_completo(costos, oferta, demanda)
        if not es_valido:
            return jsonify({
                'success': False,
                'error': 'Datos inválidos',
                'errores': errores
            }), 400
        
        # Resolver con cada método seleccionado
        resultados = {}
        
        for metodo in metodos_seleccionados:
            try:
                if metodo == 'costo_minimo':
                    solver = MetodoCostoMinimo(costos, oferta, demanda)
                elif metodo == 'esquina_noroeste':
                    solver = MetodoEsquinaNoroeste(costos, oferta, demanda)
                elif metodo == 'vogel':
                    solver = MetodoVogel(costos, oferta, demanda)
                elif metodo == 'russell':
                    solver = MetodoRussell(costos, oferta, demanda)
                else:
                    continue
                
                # Resolver el problema
                resultado = solver.resolver()
                resultados[metodo] = resultado
                
            except Exception as e:
                resultados[metodo] = {
                    'error': f'Error al resolver con {metodo}: {str(e)}'
                }
        
        # Crear resumen comparativo
        resumen_comparativo = crear_resumen_comparativo(resultados)
        
        # Información del problema original
        info_problema = {
            'costos_originales': costos,
            'oferta_original': oferta,
            'demanda_original': demanda,
            'dimensiones': f"{len(oferta)}x{len(demanda)}",
            'oferta_total': sum(oferta),
            'demanda_total': sum(demanda),
            'balanceado': abs(sum(oferta) - sum(demanda)) < 1e-6
        }
        
        return jsonify({
            'success': True,
            'problema': info_problema,
            'resultados': resultados,
            'resumen_comparativo': resumen_comparativo,
            'metodos_resueltos': list(resultados.keys())
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error general: {str(e)}'
        }), 500

#Los datos de ejmplo
@main_bp.route('/ejemplo/<int:numero>')
def obtener_ejemplo(numero):
    try:
        if numero == 1:
            # Ejemplo basado en el archivo Excel 1
            datos_ejemplo = {
                'costos': [
                    [700, 800, 500, 200],
                    [200, 900, 100, 400],
                    [400, 500, 300, 100],
                    [200, 100, 400, 300]
                ],
                'oferta': [10, 20, 20, 10],
                'demanda': [20, 10, 10, 20],
                'descripcion': 'Ejemplo 4x4 basado en datos reales de logística'
            }
        elif numero == 2:
            # Ejemplo más simple 3x3
            datos_ejemplo = {
                'costos': [
                    [4, 2, 8],
                    [6, 3, 1],
                    [2, 5, 9]
                ],
                'oferta': [30, 40, 20],
                'demanda': [20, 35, 35],
                'descripcion': 'Ejemplo 3x3 simple para aprendizaje'
            }
        else:
            return jsonify({'error': 'Número de ejemplo no válido'}), 404
        
        return jsonify({
            'success': True,
            'datos': datos_ejemplo
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al obtener ejemplo: {str(e)}'
        }), 500

#Obtenemos informaicon del os metodos disponoles
@main_bp.route('/metodos')
def informacion_metodos():
    metodos_info = {
        'costo_minimo': {
            'nombre': 'Costo Mínimo',
            'descripcion': 'Asigna siempre al costo unitario más bajo disponible',
            'complejidad': 'O(mn log(mn))',
            'ventajas': [
                'Tiende a encontrar soluciones de bajo costo',
                'Lógica intuitiva y fácil de seguir',
                'Buena calidad de solución'
            ],
            'desventajas': [
                'No garantiza la solución óptima',
                'Puede quedar atrapado en óptimos locales'
            ]
        },
        'esquina_noroeste': {
            'nombre': 'Esquina Noroeste',
            'descripcion': 'Avanza sistemáticamente desde la esquina superior izquierda',
            'complejidad': 'O(m+n)',
            'ventajas': [
                'Muy simple de implementar',
                'Rápido de ejecutar',
                'Siempre encuentra una solución factible'
            ],
            'desventajas': [
                'Ignora completamente los costos',
                'Generalmente produce soluciones costosas'
            ]
        },
        'vogel': {
            'nombre': 'Aproximación de Vogel (VAM)',
            'descripcion': 'Usa penalizaciones basadas en diferencias de costos',
            'complejidad': 'O(m²n²)',
            'ventajas': [
                'Muy buena calidad de solución',
                'Considera costos de oportunidad',
                'Balanceo entre costo y flexibilidad'
            ],
            'desventajas': [
                'Más complejo de calcular',
                'Requiere más tiempo de ejecución'
            ]
        },
        'russell': {
            'nombre': 'Método de Russell',
            'descripción': 'Usa índices ui y vj basados en máximos de filas y columnas',
            'complejidad': 'O(m²n²)',
            'ventajas': [
                'Considera patrones globales',
                'Buena calidad de solución',
                'Enfoque matemáticamente sólido'
            ],
            'desventajas': [
                'Moderadamente complejo',
                'Requiere recalcular índices en cada iteración'
            ]
        }
    }
    
    return jsonify({
        'success': True,
        'metodos': metodos_info
    })
