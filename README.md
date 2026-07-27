# TransporteIO  Solver de Problemas de Transporte

Aplicación web construida con **Flask** que resuelve problemas de transporte (Investigación de Operaciones) mediante distintos métodos de optimización, incluyendo visualización interactiva de la red de distribución.

## Funcionalidades

- Resolución de problemas de transporte con 4 métodos:
  - Costo Mínimo
  - Esquina Noroeste
  - Aproximación de Vogel (VAM)
  - Russell
- Ingreso de matriz de costos, oferta y demanda desde la interfaz web
- Validación de que la matriz cumpla las condiciones del problema de transporte
- Visualización gráfica de la red de distribución (JS)
- Endpoint de salud (`/health`) para verificar el estado del servicio

## Stack técnico

- Python 3 / Flask
- NumPy (cálculos de la matriz de transporte)
- JavaScript (visualización de red) + HTML/CSS

## Estructura

```
app.py                          # Configuración y factory de la app Flask
routes/main.py                  # Rutas principales
models/
  ---costo_minimo.py
  ---esquina_noroeste.py
  ---russell.py
  ---vogel.py
  ----transporte_base.py        # Clase base compartida por los métodos
static/js/network-visualization.js  # Visualización de la red
templates/index.html            # Interfaz principal
```

## Cómo ejecutarlo

```bash
git clone https://github.com/SirRose23/CarlosGarciaProyectoIO.git
cd CarlosGarciaProyectoIO
pip install -r requirements.txt
python app.py
```

La app corre en `http://localhost:5000`.

## Contexto

Proyecto de la asignatura de Investigación de Operaciones Universidad Mesoamericana, 2025. Debe ingresarse una matriz de costos que cumpla con las condiciones del problema de transporte (oferta = demanda) para obtener la solución óptima según el método seleccionado.
