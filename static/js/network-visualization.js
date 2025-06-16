function generarModeloRedVisual(data) {
    const networkContainer = document.getElementById('network-model');
    
    if (!resultadosActuales || !resultadosActuales.resultados) {
        mostrarPlaceholderRed(networkContainer);
        return;
    }
    
    try {
        // Encontrar el mejor método
        const metodos = Object.keys(resultadosActuales.resultados);
        const mejorMetodo = metodos.reduce((mejor, actual) => {
            return resultadosActuales.resultados[actual].costo_total < 
                   resultadosActuales.resultados[mejor].costo_total ? actual : mejor;
        });
        
        const mejorSolucion = resultadosActuales.resultados[mejorMetodo].matriz_solucion;
        const mejorCosto = resultadosActuales.resultados[mejorMetodo].costo_total;
        
        // Crear el HTML completo
        let html = '<div style="text-align: center; width: 100%;">';
        html += '<h4><i class="fas fa-project-diagram"></i> Modelo de Red del Problema</h4>';
        
        // Crear el SVG
        html += crearDiagramaRed(mejorSolucion, mejorMetodo);
        
        html += '</div>';
        
        networkContainer.innerHTML = html;
        
    } catch (error) {
        console.error('Error generando modelo de red:', error);
        mostrarErrorRed(networkContainer);
    }
}

//Creamos el diagrama de red
function crearDiagramaRed(solucionMatrix, metodo) {
    const width = 700;
    const height = 400;
    const margenX = 100;
    const margenY = 80;
    
    const numOrigenes = problemData.origenes;
    const numDestinos = problemData.destinos;
    
    // Posiciones
    const origenX = margenX;
    const destinoX = width - margenX;
    const espacioY = Math.max((height - 2 * margenY) / Math.max((Math.max(numOrigenes, numDestinos) - 1), 1), 40);
    
    let svg = `<svg width="${width}" height="${height}" style="border: 1px solid #ddd; border-radius: 10px; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); margin: 20px auto; display: block;">`;
    
    // Definir marcadores para flechas
    svg += `
        <defs>
            <marker id="arrow" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
                <polygon points="0 0, 8 3, 0 6" fill="#495057" />
            </marker>
        </defs>
    `;
    
    // Títulos de las columnas
    svg += `<text x="${origenX}" y="30" text-anchor="middle" style="font-weight: bold; font-size: 16px; fill: #495057;">ORÍGENES</text>`;
    svg += `<text x="${destinoX}" y="30" text-anchor="middle" style="font-weight: bold; font-size: 16px; fill: #495057;">DESTINOS</text>`;
    
    // Dibujar TODAS las conexiones con sus costos
    for (let i = 0; i < numOrigenes; i++) {
        const origenY = margenY + (i * espacioY);
        
        for (let j = 0; j < numDestinos; j++) {
            const destinoY = margenY + (j * espacioY);
            const costo = problemData.costos[i][j];
            
            const midX = (origenX + 30 + destinoX - 30) / 2;
            const midY = (origenY + destinoY) / 2;
            
            // Todas las conexiones con el mismo estilo
            svg += `<line x1="${origenX + 30}" y1="${origenY}" x2="${destinoX - 30}" y2="${destinoY}" 
                    stroke="#495057" stroke-width="2" marker-end="url(#arrow)" opacity="0.7"/>`;
            
            // Etiqueta con el costo unitario
            svg += `<rect x="${midX - 25}" y="${midY - 10}" width="50" height="20" 
                    fill="white" stroke="#495057" stroke-width="1" rx="5" opacity="0.9"/>`;
            svg += `<text x="${midX}" y="${midY + 3}" text-anchor="middle" 
                    style="font-size: 11px; font-weight: bold; fill: #495057;">${formatearNumero(costo)}</text>`;
        }
    }
    
    // Dibujar nodos de orígenes
    for (let i = 0; i < numOrigenes; i++) {
        const y = margenY + (i * espacioY);
        
        // Círculo principal
        svg += `<circle cx="${origenX}" cy="${y}" r="28" fill="#667eea" stroke="#495057" stroke-width="2"/>`;
        svg += `<text x="${origenX}" y="${y + 5}" text-anchor="middle" 
                style="font-size: 18px; font-weight: bold; fill: white;">${i + 1}</text>`;
        
        // Etiqueta y oferta
        svg += `<text x="${origenX - 55}" y="${y + 5}" text-anchor="middle" 
                style="font-size: 14px; font-weight: bold; fill: #495057;">P${i + 1}</text>`;
        svg += `<text x="${origenX - 55}" y="${y + 20}" text-anchor="middle" 
                style="font-size: 11px; fill: #6c757d;">[${formatearNumero(problemData.oferta[i])}]</text>`;
    }
    
    // Dibujar nodos de destinos
    for (let j = 0; j < numDestinos; j++) {
        const y = margenY + (j * espacioY);
        
        // Círculo principal
        svg += `<circle cx="${destinoX}" cy="${y}" r="28" fill="#764ba2" stroke="#495057" stroke-width="2"/>`;
        svg += `<text x="${destinoX}" y="${y + 5}" text-anchor="middle" 
                style="font-size: 18px; font-weight: bold; fill: white;">${j + 1}</text>`;
        
        // Etiqueta y demanda
        svg += `<text x="${destinoX + 55}" y="${y + 5}" text-anchor="middle" 
                style="font-size: 14px; font-weight: bold; fill: #495057;">T${j + 1}</text>`;
        svg += `<text x="${destinoX + 55}" y="${y + 20}" text-anchor="middle" 
                style="font-size: 11px; fill: #6c757d;">[${formatearNumero(problemData.demanda[j])}]</text>`;
    }
    
    // Leyenda simplificada
    const leyendaY = height - 25;
    svg += `<rect x="10" y="${leyendaY - 15}" width="${width - 20}" height="25" 
            fill="white" stroke="#dee2e6" rx="8" opacity="0.95"/>`;
    
    svg += `<text x="20" y="${leyendaY - 3}" style="font-size: 12px; fill: #495057;">
            Modelo de Red - Costos de Transporte</text>`;
    
    svg += `<text x="${width - 20}" y="${leyendaY - 3}" text-anchor="end" 
            style="font-size: 12px; font-weight: bold; fill: #667eea;">
            Método: ${metodo.replace('_', ' ').toUpperCase()}</text>`;
    
    svg += '</svg>';
    
    return svg;
}



//Si no hay resultados, mostramos un placeholder
function mostrarPlaceholderRed(container) {
    container.innerHTML = `
        <div class="network-placeholder">
            <i class="fas fa-project-diagram fa-3x"></i>
            <p>El modelo de red se generará después de resolver el problema</p>
            <p style="font-size: 0.9rem; color: #888; margin-top: 10px;">
                Utiliza los botones de "Validar" y "Resolver" para generar la visualización
            </p>
        </div>
    `;
}

/**
 * Mostrar error en la visualización
 */
function mostrarErrorRed(container) {
    container.innerHTML = `
        <div class="network-placeholder">
            <i class="fas fa-exclamation-triangle fa-3x" style="color: #dc3545;"></i>
            <p style="color: #dc3545;">Error al generar el modelo de red</p>
            <p style="font-size: 0.9rem; color: #888;">
                Intenta resolver el problema nuevamente
            </p>
        </div>
    `;
}

// Función de compatibilidad
function generarModeloRed(data) {
    generarModeloRedVisual(data);
}
