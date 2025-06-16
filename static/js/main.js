// Variables globales
let problemData = {
    costos: [],
    oferta: [],
    demanda: [],
    origenes: 4,
    destinos: 4
};

let metodosSeleccionados = ['costo_minimo', 'esquina_noroeste', 'vogel', 'russell'];
let resultadosActuales = null;

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 TransporteIO iniciado');
    configurarEventListeners();
    mostrarBienvenida();
});

 //Configurar listeners
function configurarEventListeners() {
    // Selección de métodos
    document.querySelectorAll('.method-card').forEach(card => {
        card.addEventListener('click', function() {
            toggleMetodo(this.dataset.method, this);
        });
    });
    
    // Inputs de dimensiones
    document.getElementById('num-origenes').addEventListener('change', validarDimensiones);
    document.getElementById('num-destinos').addEventListener('change', validarDimensiones);
    
    // Atajos de teclado
    document.addEventListener('keydown', manejarAtajos);
}

//Seleccion del metodo
function toggleMetodo(metodo, elemento) {
    elemento.classList.toggle('selected');
    
    if (elemento.classList.contains('selected')) {
        if (!metodosSeleccionados.includes(metodo)) {
            metodosSeleccionados.push(metodo);
        }
    } else {
        metodosSeleccionados = metodosSeleccionados.filter(m => m !== metodo);
    }
    
    console.log('Métodos seleccionados:', metodosSeleccionados);
}

// Validacion de ls dimenciones
function validarDimensiones() {
    const origenes = parseInt(document.getElementById('num-origenes').value);
    const destinos = parseInt(document.getElementById('num-destinos').value);
    
    if (origenes < 2 || origenes > 8 || destinos < 2 || destinos > 8) {
        mostrarError('Las dimensiones deben estar entre 2 y 8');
        return false;
    }
    
    return true;
}

//Generamos la matriz de entrada
function generarMatriz() {
    if (!validarDimensiones()) return;
    
    const origenes = parseInt(document.getElementById('num-origenes').value);
    const destinos = parseInt(document.getElementById('num-destinos').value);
    
    problemData.origenes = origenes;
    problemData.destinos = destinos;
    
    // Inicializar matrices
    problemData.costos = Array(origenes).fill().map(() => Array(destinos).fill(0));
    problemData.oferta = Array(origenes).fill(0);
    problemData.demanda = Array(destinos).fill(0);
    
    generarTablaMatriz();
    
    // Mostrar matriz y ocultar bienvenida
    document.getElementById('welcome-message').style.display = 'none';
    document.getElementById('matriz-container').style.display = 'block';
    
    mostrarExito(`Matriz ${origenes}×${destinos} generada exitosamente`);
}

//Generamos la tabla html para la matriz
function generarTablaMatriz() {
    const container = document.getElementById('matriz-datos');
    const { origenes, destinos } = problemData;
    
    let html = '<table class="matrix-table">';
    
    // Encabezado
    html += '<thead><tr><th>O\\D</th>';
    for (let j = 0; j < destinos; j++) {
        html += `<th>T${j + 1}</th>`;
    }
    html += '<th>Oferta</th></tr></thead><tbody>';
    
    // Filas de orígenes
    for (let i = 0; i < origenes; i++) {
        html += `<tr><td><strong>P${i + 1}</strong></td>`;
        
        // Celdas de costos
        for (let j = 0; j < destinos; j++) {
            html += `<td><input type="number" class="matrix-input" 
                      id="costo_${i}_${j}" value="0" min="0" step="0.01" 
                      placeholder="Costo" onchange="actualizarCosto(${i}, ${j}, this.value)"></td>`;
        }
        
        // Celda de oferta
        html += `<td><input type="number" class="matrix-input" 
                  id="oferta_${i}" value="0" min="0" step="0.01" 
                  placeholder="Oferta" onchange="actualizarOferta(${i}, this.value)"></td>`;
        html += '</tr>';
    }
    
    // Fila de demanda
    html += '<tr><td><strong>Demanda</strong></td>';
    for (let j = 0; j < destinos; j++) {
        html += `<td><input type="number" class="matrix-input" 
                  id="demanda_${j}" value="0" min="0" step="0.01" 
                  placeholder="Demanda" onchange="actualizarDemanda(${j}, this.value)"></td>`;
    }
    html += '<td><strong>Total</strong></td></tr>';
    
    html += '</tbody></table>';
    container.innerHTML = html;
}

//Actualizamos el costo de la matriz
function actualizarCosto(i, j, valor) {
    problemData.costos[i][j] = parseFloat(valor) || 0;
}

//Actualizamos la oferta para la matriz
function actualizarOferta(i, valor) {
    problemData.oferta[i] = parseFloat(valor) || 0;
}

//Actualizamos la demanda para la matriz
function actualizarDemanda(j, valor) {
    problemData.demanda[j] = parseFloat(valor) || 0;
}

//valiadmos los datos ingresados
async function validarDatos() {
    if (!problemData.costos.length) {
        mostrarError('Primero genera una matriz');
        return;
    }
    
    try {
        const response = await fetch('/validar', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(problemData)
        });
        
        const result = await response.json();
        
        if (result.valido) {
            mostrarExito('✅ Datos válidos. El problema está balanceado.');
            document.getElementById('btn-resolver').disabled = false;
        } else {
            mostrarError('❌ Errores encontrados:<br>' + result.errores.join('<br>'));
            document.getElementById('btn-resolver').disabled = true;
        }
        
    } catch (error) {
        mostrarError('Error en la validación: ' + error.message);
    }
}

//Resolucion con los metodos seleccionados
async function resolverProblema() {
    if (metodosSeleccionados.length === 0) {
        mostrarError('Selecciona al menos un método');
        return;
    }
    
    // Mostrar loading
    mostrarLoading(true);
    
    try {
        const response = await fetch('/resolver', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                costos: problemData.costos,
                oferta: problemData.oferta,
                demanda: problemData.demanda,
                metodos: metodosSeleccionados
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            resultadosActuales = result;
            mostrarResultados(result);
        } else {
            mostrarError('Error al resolver: ' + result.error);
        }
        
    } catch (error) {
        mostrarError('Error en la resolución: ' + error.message);
    } finally {
        mostrarLoading(false);
    }
}

//Cargar ejemplos
async function cargarEjemplo(numero) {
    try {
        const response = await fetch(`/ejemplo/${numero}`);
        const result = await response.json();
        
        if (result.success) {
            const datos = result.datos;
            
            // Actualizar dimensiones
            document.getElementById('num-origenes').value = datos.oferta.length;
            document.getElementById('num-destinos').value = datos.demanda.length;
            
            // Generar matriz
            generarMatriz();
            
            // Llenar datos
            setTimeout(() => {
                llenarDatosEjemplo(datos);
                mostrarExito(`📋 ${datos.descripcion} cargado exitosamente`);
            }, 100);
        } else {
            mostrarError('Error al cargar ejemplo: ' + result.error);
        }
        
    } catch (error) {
        mostrarError('Error al cargar ejemplo: ' + error.message);
    }
}

//LLenar con datos de ejemplo
function llenarDatosEjemplo(datos) {
    const { costos, oferta, demanda } = datos;
    
    // Llenar costos
    for (let i = 0; i < costos.length; i++) {
        for (let j = 0; j < costos[i].length; j++) {
            const input = document.getElementById(`costo_${i}_${j}`);
            if (input) {
                input.value = costos[i][j];
                problemData.costos[i][j] = costos[i][j];
            }
        }
    }
    
    // Llenar ofertas
    for (let i = 0; i < oferta.length; i++) {
        const input = document.getElementById(`oferta_${i}`);
        if (input) {
            input.value = oferta[i];
            problemData.oferta[i] = oferta[i];
        }
    }
    
    // Llenar demandas
    for (let j = 0; j < demanda.length; j++) {
        const input = document.getElementById(`demanda_${j}`);
        if (input) {
            input.value = demanda[j];
            problemData.demanda[j] = demanda[j];
        }
    }
}
//limpiamos
function limpiarTodo() {
    // Resetear datos
    problemData = {
        costos: [],
        oferta: [],
        demanda: [],
        origenes: 4,
        destinos: 4
    };
    
    resultadosActuales = null;
    
    // Resetear interfaz
    document.getElementById('num-origenes').value = 4;
    document.getElementById('num-destinos').value = 4;
    document.getElementById('welcome-message').style.display = 'block';
    document.getElementById('matriz-container').style.display = 'none';
    document.getElementById('resultados-container').style.display = 'none';
    document.getElementById('btn-resolver').disabled = true;
    
    limpiarMensajes();
    mostrarExito('🧹 Todo limpiado exitosamente');
}

// Mostrar u oucltar clavitos
function mostrarLoading(mostrar) {
    const loading = document.getElementById('loading');
    const progressFill = document.getElementById('progress-fill');
    
    if (mostrar) {
        loading.classList.add('show');
        document.getElementById('resultados-container').style.display = 'none';
        
        // Simular progreso
        let progress = 0;
        const interval = setInterval(() => {
            progress += 10;
            progressFill.style.width = progress + '%';
            if (progress >= 100) {
                clearInterval(interval);
            }
        }, 200);
        
    } else {
        loading.classList.remove('show');
        progressFill.style.width = '0%';
    }
}

//mosntramos bienvenida
function mostrarBienvenida() {
    document.getElementById('welcome-message').style.display = 'block';
    document.getElementById('matriz-container').style.display = 'none';
    document.getElementById('resultados-container').style.display = 'none';
}

//atajaos de teclado
function manejarAtajos(e) {
    if (e.ctrlKey) {
        switch(e.key) {
            case 'Enter':
                e.preventDefault();
                if (!document.getElementById('btn-resolver').disabled) {
                    resolverProblema();
                }
                break;
            case 'r':
                e.preventDefault();
                limpiarTodo();
                break;
            case 'v':
                e.preventDefault();
                validarDatos();
                break;
        }
    }
}
console.log('🎮 Atajos de teclado:');
console.log('Ctrl + Enter: Resolver problema');
console.log('Ctrl + R: Limpiar todo');
console.log('Ctrl + V: Validar datos');
