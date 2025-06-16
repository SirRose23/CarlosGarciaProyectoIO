function mostrarResultados(data) {
    const container = document.getElementById('resultados-container');
    const detalladosContainer = document.getElementById('resultados-detallados');
    const comparacionContainer = document.getElementById('tabla-comparacion');
    
    // Generar tabla de comparación
    generarTablaComparacion(data.resultados, comparacionContainer);
    
    // Generar resultados detallados
    let htmlDetallado = '';
    Object.entries(data.resultados).forEach(([metodo, resultado]) => {
        htmlDetallado += generarTarjetaResultado(resultado);
    });
    
    detalladosContainer.innerHTML = htmlDetallado;
    container.style.display = 'block';
    
    // Generar modelo de red VISUAL
    generarModeloRedVisual(data);
    
    // Scroll hacia resultados
    container.scrollIntoView({ behavior: 'smooth' });
    
    // Inicializar pestañas después de un pequeño delay
    setTimeout(() => {
        inicializarPestanasPasos();
    }, 100);
    
    // Animar entrada
    animarFadeIn(container);
}

//Tabla de comparacion de metodos
function generarTablaComparacion(resultados, container) {
    const metodos = Object.keys(resultados);
    
    let html = '<h3><i class="fas fa-balance-scale"></i> Comparación de Métodos</h3>';
    html += '<table class="comparison-table">';
    html += '<thead><tr><th>Método</th><th>Costo Total</th></tr></thead><tbody>';
    
    metodos.forEach(metodo => {
        const resultado = resultados[metodo];
        
        html += `<tr>`;
        html += `<td><strong>${resultado.metodo}</strong></td>`;
        html += `<td>${formatearMoneda(resultado.costo_total)}</td>`;
        html += '</tr>';
    });
    
    html += '</tbody></table>';
    container.innerHTML = html;
}

//Tarjeta de resultados por metodo
function generarTarjetaResultado(resultado) {
    let html = `<div class="result-card">`;
    html += `<div class="result-header">`;
    html += `<h3 class="result-title"><i class="fas fa-calculator"></i> ${resultado.metodo}</h3>`;
    html += `<div class="result-cost">${formatearMoneda(resultado.costo_total)}</div>`;
    html += `</div>`;
    
    // Matriz solución final
    html += '<h4><i class="fas fa-table"></i> Matriz de Asignación Final:</h4>';
    html += generarTablaMatrizSolucion(resultado.matriz_solucion);
    
    // Pasos del proceso con visualización paso a paso
    html += generarPasosVisuales(resultado);
    
    html += `</div>`;
    return html;
}

//Tabla matriz de solucion
function generarTablaMatrizSolucion(matriz) {
    const { origenes, destinos } = problemData;
    
    let html = '<table class="matrix-step-table" style="margin-bottom: 20px;">';
    
    // Header con demanda (igual que en paso a paso)
    html += '<thead><tr><th>O\\D</th>';
    for (let j = 0; j < destinos; j++) {
        html += `<th>T${j + 1}<br><small>Dem: ${formatearNumero(problemData.demanda[j])}</small></th>`;
    }
    html += '<th>Oferta</th></tr></thead>';
    
    // Cuerpo con el mismo estilo que paso a paso
    html += '<tbody>';
    for (let i = 0; i < origenes; i++) {
        html += '<tr>';
        html += `<td><strong>P${i + 1}</strong></td>`;
        
        for (let j = 0; j < destinos; j++) {
            const valor = matriz[i][j];
            
            // Usar las mismas clases que en paso a paso
            let claseExtra = '';
            if (valor > 0) {
                claseExtra = 'celda-asignada';
            } else {
                claseExtra = 'celda-vacia';
            }
            
            html += `<td class="${claseExtra}">`;
            
            // SOLO mostrar las asignaciones, igual que paso a paso
            if (valor > 0) {
                html += `<span class="asignacion-grande">${formatearNumero(valor)}</span>`;
            } else {
                html += `<span class="asignacion-cero">0</span>`;
            }
            
            html += `</td>`;
        }
        
        // Columna de oferta
        html += `<td><strong>${formatearNumero(problemData.oferta[i])}</strong></td>`;
        html += '</tr>';
    }
    
    html += '</tbody></table>';
    return html;
}

//Modelo de red
function generarModeloRed(data) {
    const networkContainer = document.getElementById('network-model');
    
    let html = '<div style="text-align: left;">';
    html += '<h4><i class="fas fa-project-diagram"></i> Modelo de Red del Problema</h4>';
    html += '<div style="background: white; padding: 15px; border-radius: 10px; margin: 10px 0;">';
    
    html += '<p><strong>Estructura del problema:</strong></p>';
    html += `<ul style="margin: 10px 0; padding-left: 20px;">`;
    html += `<li>Orígenes: ${problemData.origenes} (P1 - P${problemData.origenes})</li>`;
    html += `<li>Destinos: ${problemData.destinos} (T1 - T${problemData.destinos})</li>`;
    html += `<li>Oferta total: ${formatearNumero(problemData.oferta.reduce((a, b) => a + b, 0))}</li>`;
    html += `<li>Demanda total: ${formatearNumero(problemData.demanda.reduce((a, b) => a + b, 0))}</li>`;
    html += '</ul>';
    
    html += '<p><strong>Conexiones principales (con asignación > 0):</strong></p>';
    
    // Mostrar las conexiones activas del mejor método
    if (resultadosActuales && resultadosActuales.resultados) {
        const metodos = Object.keys(resultadosActuales.resultados);
        const mejorMetodo = metodos.reduce((mejor, actual) => {
            return resultadosActuales.resultados[actual].costo_total < 
                   resultadosActuales.resultados[mejor].costo_total ? actual : mejor;
        });
        
        const mejorSolucion = resultadosActuales.resultados[mejorMetodo].matriz_solucion;
        
        html += '<ul style="margin: 10px 0; padding-left: 20px;">';
        for (let i = 0; i < problemData.origenes; i++) {
            for (let j = 0; j < problemData.destinos; j++) {
                if (mejorSolucion[i][j] > 0) {
                    const costo = problemData.costos[i][j];
                    const cantidad = mejorSolucion[i][j];
                    html += `<li>P${i + 1} → T${j + 1}: ${formatearNumero(cantidad)} unidades (costo: ${formatearMoneda(costo)} c/u)</li>`;
                }
            }
        }
        html += '</ul>';
        
        const mejorCosto = resultadosActuales.resultados[mejorMetodo].costo_total;
        html += `<p><strong>Solución óptima:</strong> ${mejorMetodo.replace('_', ' ').toUpperCase()} con costo total de ${formatearMoneda(mejorCosto)}</p>`;
    }
    
    html += '</div></div>';
    networkContainer.innerHTML = html;
}

//Grafico de compracion
function crearGraficoComparacion(resultados) {
    const canvas = document.createElement('canvas');
    canvas.width = 400;
    canvas.height = 200;
    const ctx = canvas.getContext('2d');
    
    const metodos = Object.keys(resultados);
    const costos = metodos.map(m => resultados[m].costo_total);
    const maxCosto = Math.max(...costos);
    
    // Dibujar barras simples
    const barWidth = canvas.width / metodos.length - 20;
    const barMaxHeight = canvas.height - 40;
    
    metodos.forEach((metodo, index) => {
        const altura = (costos[index] / maxCosto) * barMaxHeight;
        const x = index * (barWidth + 20) + 10;
        const y = canvas.height - altura - 20;
        
        // Barra
        ctx.fillStyle = '#667eea';
        ctx.fillRect(x, y, barWidth, altura);
        
        // Etiqueta
        ctx.fillStyle = '#333';
        ctx.font = '12px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(metodo.replace('_', ' '), x + barWidth/2, canvas.height - 5);
        
        // Valor
        ctx.fillText(formatearMoneda(costos[index]), x + barWidth/2, y - 5);
    });
    
    return canvas;
}

//Exportamos grafico como imagen
function exportarGrafico(resultados) {
    const canvas = crearGraficoComparacion(resultados);
    const link = document.createElement('a');
    link.download = 'comparacion_metodos.png';
    link.href = canvas.toDataURL();
    link.click();
    
    mostrarExito('📊 Gráfico exportado exitosamente');
}

//estadisticas avanzadas
function mostrarEstadisticasAvanzadas(resultados) {
    const metodos = Object.keys(resultados);
    const costos = metodos.map(m => resultados[m].costo_total);
    
    const estadisticas = {
        promedio: costos.reduce((a, b) => a + b, 0) / costos.length,
        minimo: Math.min(...costos),
        maximo: Math.max(...costos),
        desviacion: calcularDesviacionEstandar(costos),
        rango: Math.max(...costos) - Math.min(...costos)
    };
    
    let html = '<div class="estadisticas-avanzadas">';
    html += '<h4><i class="fas fa-chart-bar"></i> Estadísticas Avanzadas</h4>';
    html += `<p><strong>Costo Promedio:</strong> ${formatearMoneda(estadisticas.promedio)}</p>`;
    html += `<p><strong>Mejor Costo:</strong> ${formatearMoneda(estadisticas.minimo)}</p>`;
    html += `<p><strong>Peor Costo:</strong> ${formatearMoneda(estadisticas.maximo)}</p>`;
    html += `<p><strong>Rango:</strong> ${formatearMoneda(estadisticas.rango)}</p>`;
    html += `<p><strong>Desviación Estándar:</strong> ${formatearMoneda(estadisticas.desviacion)}</p>`;
    html += '</div>';
    
    return html;
}

//Desviacion estandar
function calcularDesviacionEstandar(valores) {
    const promedio = valores.reduce((a, b) => a + b, 0) / valores.length;
    const varianza = valores.reduce((sum, valor) => sum + Math.pow(valor - promedio, 2), 0) / valores.length;
    return Math.sqrt(varianza);
}

//Mostrar paso a paso
function generarPasosVisuales(resultado) {
    let html = `<div class="steps-container">`;
    html += `<h4><i class="fas fa-list-ol"></i> Proceso Paso a Paso (${resultado.pasos_detallados.length} pasos):</h4>`;
    
    // Crear un contenedor con pestañas navegables
    html += `<div class="steps-navigation">`;
    html += `<div class="steps-tabs">`;
    
    resultado.pasos_detallados.forEach((paso, index) => {
        const isActive = index === 0 ? 'active' : '';
        html += `<button class="step-tab ${isActive}" data-step="${index}" onclick="mostrarPaso(${index}, '${resultado.metodo.replace(/\s+/g, '_')}')">Paso ${index + 1}</button>`;
    });
    
    html += `</div>`;
    html += `<div class="steps-content" id="steps-content-${resultado.metodo.replace(/\s+/g, '_')}">`;
    
    resultado.pasos_detallados.forEach((paso, index) => {
        const isActive = index === 0 ? 'active' : '';
        html += `<div class="step-panel ${isActive}" data-step="${index}">`;
        html += generarPasoVisual(paso, index, resultado);
        html += `</div>`;
    });
    
    html += `</div>`;
    html += `</div>`;
    html += `</div>`;
    
    return html;
}

//Genera paso a paso
function generarPasoVisual(paso, index, resultado) {
    let html = `<div class="visual-step">`;
    
    // Header del paso
    html += `<div class="step-visual-header">`;
    html += `<h5><i class="fas fa-step-forward"></i> Paso ${index + 1}: ${paso.titulo}</h5>`;
    html += `<div class="step-cost-badge">${formatearMoneda(paso.costo_parcial || 0)}</div>`;
    html += `</div>`;
    
    // Descripción del paso
    html += `<div class="step-description-visual">`;
    html += `<p>${paso.descripcion.replace(/\\n/g, '<br>')}</p>`;
    html += `</div>`;
    
    // SIEMPRE mostrar la tabla del estado actual
    html += generarTablaEstadoPaso(paso, index, resultado);
    
    html += `</div>`;
    return html;
}

//Tabla de cada paso ap aso
function generarTablaEstadoPaso(paso, stepIndex, resultado) {
    const { origenes, destinos } = problemData;
    
    let html = `<div class="step-table-container">`;
    
    // Título dinámico según el tipo de paso
    if (stepIndex === 0) {
        html += `<h6><i class="fas fa-table"></i> Estado Inicial - Matriz de Asignación (Todos en cero):</h6>`;
    } else {
        html += `<h6><i class="fas fa-table"></i> Estado de la Matriz después del Paso ${stepIndex}:</h6>`;
    }
    
    // Reconstruir matriz hasta este paso
    const matrizPaso = reconstruirMatrizHastaPaso(resultado.pasos_detallados, stepIndex);
    
    // Para debug: mostrar el estado de la matriz
    console.log(`Estado matriz paso ${stepIndex}:`, matrizPaso);
    console.log(`Pasos disponibles hasta ${stepIndex}:`, resultado.pasos_detallados.slice(0, stepIndex + 1));
    
    html += '<table class="matrix-step-table">';
    
    // Header con demanda
    html += '<thead><tr><th>O\\D</th>';
    for (let j = 0; j < destinos; j++) {
        html += `<th>T${j + 1}<br><small>Dem: ${formatearNumero(problemData.demanda[j])}</small></th>`;
    }
    html += '<th>Oferta</th></tr></thead>';
    
    // Cuerpo de la tabla
    html += '<tbody>';
    for (let i = 0; i < origenes; i++) {
        html += '<tr>';
        html += `<td><strong>P${i + 1}</strong></td>`;
        
        for (let j = 0; j < destinos; j++) {
            const valor = matrizPaso[i][j];
            const costo = problemData.costos[i][j];
            
            // Determinar clase y estilo de la celda
            let claseExtra = '';
            let estiloExtra = '';
            
            // Resaltar celda recién asignada en este paso
            if (stepIndex > 0 && paso && paso.datos_extra && paso.datos_extra.celda_seleccionada && 
                paso.datos_extra.celda_seleccionada[0] === i && 
                paso.datos_extra.celda_seleccionada[1] === j) {
                claseExtra = 'celda-nueva-asignacion';
                estiloExtra = 'animation: highlight 3s ease-in-out;';
            } else if (valor > 0) {
                claseExtra = 'celda-asignada';
            } else {
                claseExtra = 'celda-vacia';
            }
            
            html += `<td class="${claseExtra}" style="${estiloExtra}">`;
            
            // SOLO mostrar las asignaciones, sin costos unitarios
            if (valor > 0) {
                html += `<span class="asignacion-grande">${formatearNumero(valor)}</span>`;
            } else {
                html += `<span class="asignacion-cero">0</span>`;
            }
            
            html += `</td>`;
        }
        
        // Columna de oferta
        html += `<td><strong>${formatearNumero(problemData.oferta[i])}</strong></td>`;
        html += '</tr>';
    }
    
    html += '</tbody></table>';
    
    // Información adicional del paso
    if (stepIndex > 0 && paso && paso.datos_extra && paso.datos_extra.celda_seleccionada && paso.datos_extra.cantidad_asignada) {
        const [fila, col] = paso.datos_extra.celda_seleccionada;
        const cantidad = paso.datos_extra.cantidad_asignada;
        const costoUnitario = problemData.costos[fila][col];
        const costoTotal = cantidad * costoUnitario;
        
        html += `<div class="step-info-additional">`;
        html += `<div class="assignment-details">`;
        html += `<h6><i class="fas fa-info-circle"></i> Última Asignación Realizada:</h6>`;
        html += `<div class="assignment-grid">`;
        html += `<div class="detail-item">`;
        html += `<span class="label">Ruta seleccionada:</span>`;
        html += `<span class="value">P${fila + 1} → T${col + 1}</span>`;
        html += `</div>`;
        html += `<div class="detail-item">`;
        html += `<span class="label">Cantidad asignada:</span>`;
        html += `<span class="value">${formatearNumero(cantidad)} unidades</span>`;
        html += `</div>`;
        html += `<div class="detail-item">`;
        html += `<span class="label">Costo unitario:</span>`;
        html += `<span class="value">${formatearMoneda(costoUnitario)}</span>`;
        html += `</div>`;
        html += `<div class="detail-item">`;
        html += `<span class="label">Costo de este paso:</span>`;
        html += `<span class="value highlight">${formatearMoneda(costoTotal)}</span>`;
        html += `</div>`;
        html += `</div>`;
        html += `</div>`;
        html += `</div>`;
    }
    
    html += `</div>`;
    
    return html;
}



//Reconstruccion de la matriz
function reconstruirMatrizHastaPaso(pasos, hastaIndice) {
    const { origenes, destinos } = problemData;
    const matriz = Array(origenes).fill().map(() => Array(destinos).fill(0));
    
    console.log(`=== RECONSTRUYENDO MATRIZ HASTA PASO ${hastaIndice} ===`);
    console.log('Pasos totales:', pasos.length);
    
    // Acumular todas las asignaciones desde el paso 1 hasta el paso actual
    for (let i = 1; i <= hastaIndice; i++) {
        const paso = pasos[i];
        
        console.log(`Procesando paso ${i}:`, paso);
        
        // Verificar que el paso tiene los datos necesarios
        if (paso && paso.datos_extra && paso.datos_extra.celda_seleccionada && typeof paso.datos_extra.cantidad_asignada !== 'undefined') {
            const [fila, col] = paso.datos_extra.celda_seleccionada;
            const cantidad = paso.datos_extra.cantidad_asignada;
            
            console.log(`  - Celda: [${fila}, ${col}], Cantidad: ${cantidad}`);
            
            // Validar índices
            if (fila >= 0 && fila < origenes && col >= 0 && col < destinos && cantidad > 0) {
                matriz[fila][col] += cantidad;
                console.log(`  ✓ Asignando ${cantidad} a P${fila+1}->T${col+1}. Matriz[${fila}][${col}] = ${matriz[fila][col]}`);
            } else {
                console.log(`  ✗ Índices inválidos o cantidad cero`);
            }
        } else {
            console.log(`  ✗ Paso ${i} no tiene datos de asignación:`, {
                tiene_paso: !!paso,
                tiene_datos_extra: !!(paso && paso.datos_extra),
                tiene_celda: !!(paso && paso.datos_extra && paso.datos_extra.celda_seleccionada),
                tiene_cantidad: !!(paso && paso.datos_extra && typeof paso.datos_extra.cantidad_asignada !== 'undefined')
            });
        }
    }
    
    console.log('Matriz final reconstruida:', matriz);
    console.log('==============================');
    
    return matriz;
}

//Pasos especificos
function mostrarPaso(stepIndex, metodo) {
    const container = document.getElementById(`steps-content-${metodo}`);
    const tabs = container.parentElement.querySelectorAll('.step-tab');
    const panels = container.querySelectorAll('.step-panel');
    
    // Actualizar pestañas
    tabs.forEach(tab => tab.classList.remove('active'));
    tabs[stepIndex].classList.add('active');
    
    // Actualizar paneles
    panels.forEach(panel => panel.classList.remove('active'));
    panels[stepIndex].classList.add('active');
}

//PEstanas de pasos
function inicializarPestanasPasos() {
    // Esta función se ejecuta después de que se cargan los resultados
    console.log('Pestañas de pasos inicializadas');
}