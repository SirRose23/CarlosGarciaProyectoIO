function mostrarError(mensaje) {
    limpiarMensajes();
    const div = document.createElement('div');
    div.className = 'error';
    div.innerHTML = mensaje;
    document.querySelector('.control-panel').appendChild(div);
    
    setTimeout(() => {
        if (div.parentNode) {
            div.parentNode.removeChild(div);
        }
    }, 5000);
}

//MEnsajes de exito
function mostrarExito(mensaje) {
    limpiarMensajes();
    const div = document.createElement('div');
    div.className = 'success';
    div.innerHTML = mensaje;
    document.querySelector('.control-panel').appendChild(div);
    
    setTimeout(() => {
        if (div.parentNode) {
            div.parentNode.removeChild(div);
        }
    }, 3000);
}

//Limpiamos mensajes
function limpiarMensajes() {
    const mensajes = document.querySelectorAll('.error, .success, .warning');
    mensajes.forEach(el => {
        if (el.parentNode) {
            el.parentNode.removeChild(el);
        }
    });
}

//Pasamos la moneda a GT
function formatearMoneda(numero) {
    return `$${numero.toLocaleString('es-GT', {minimumFractionDigits: 2})}`;
}

//Numero con separadores
function formatearNumero(numero, decimales = 2) {
    return numero.toLocaleString('es-GT', {
        minimumFractionDigits: decimales,
        maximumFractionDigits: decimales
    });
}

//Animacion
function animarFadeIn(elemento) {
    elemento.style.opacity = '0';
    elemento.style.transform = 'translateY(20px)';
    elemento.style.transition = 'all 0.5s ease';
    
    setTimeout(() => {
        elemento.style.opacity = '1';
        elemento.style.transform = 'translateY(0)';
    }, 100);
}

//Restaltamos un elementos
function resaltarElemento(selector, duracion = 2000) {
    const elemento = document.querySelector(selector);
    if (elemento) {
        elemento.style.transition = 'all 0.3s ease';
        elemento.style.transform = 'scale(1.05)';
        elemento.style.boxShadow = '0 0 20px rgba(102, 126, 234, 0.5)';
        
        setTimeout(() => {
            elemento.style.transform = 'scale(1)';
            elemento.style.boxShadow = '';
        }, duracion);
    }
}

//Valiamos entrada numerica
function validarEntradaNumerica(input, min = 0, max = Infinity) {
    const valor = parseFloat(input.value);
    
    if (isNaN(valor) || valor < min || valor > max) {
        input.style.borderColor = '#dc3545';
        input.style.backgroundColor = '#fff5f5';
        return false;
    } else {
        input.style.borderColor = '#28a745';
        input.style.backgroundColor = '#f0fff4';
        return true;
    }
}

//Exportamos resultados a JSON
function exportarResultados() {
    if (!resultadosActuales) {
        mostrarError('No hay resultados para exportar');
        return;
    }
    
    const dataStr = JSON.stringify(resultadosActuales, null, 2);
    const dataBlob = new Blob([dataStr], {type: 'application/json'});
    
    const link = document.createElement('a');
    link.href = URL.createObjectURL(dataBlob);
    link.download = `resultados_transporte_${new Date().toISOString().split('T')[0]}.json`;
    link.click();
    
    mostrarExito('📥 Resultados exportados exitosamente');
}

//debug
window.debugInfo = function() {
    console.log('Problem Data:', problemData);
    console.log('Métodos Seleccionados:', metodosSeleccionados);
    console.log('Resultados Actuales:', resultadosActuales);
};
