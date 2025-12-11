let rutaActual = '';

// Cargar ruta de documentos por defecto
async function cargarRutaDocumentos() {
    try {
        const ruta = await eel.obtener_ruta_documentos()();
        document.getElementById('rutaInput').value = ruta;
        // No establecer rutaActual ni mostrar vista previa automáticamente
        // El usuario debe hacer clic en "Establecer"
    } catch (error) {
        console.error('Error al cargar la ruta de documentos: ' + error);
    }
}

// Establecer ruta manual
async function establecerRutaManual() {
    const input = document.getElementById('rutaInput').value.trim();
    
    if (!input) {
        mostrarError('Por favor, ingresa una ruta válida');
        return;
    }
    
    try {
        const resultado = await eel.establecer_ruta(input)();
        
        if (resultado.success) {
            rutaActual = input;
            await mostrarVistaPrevia(input);
        } else {
            mostrarError(resultado.mensaje);
        }
    } catch (error) {
        mostrarError('Error al establecer la ruta: ' + error);
    }
}

// Mostrar vista previa de archivos
async function mostrarVistaPrevia(ruta) {
    try {
        const resultado = await eel.obtener_vista_previa(ruta)();
        
        if (!resultado.success) {
            mostrarError(resultado.mensaje);
            return;
        }
        
        const previewCard = document.getElementById('previewCard');
        const previewContent = document.getElementById('previewContent');
        
        previewContent.innerHTML = '';
        
        const preview = resultado.preview;
        const categorias = Object.keys(preview);
        
        // Mostrar información de archivos omitidos
        if (resultado.omitidos > 0) {
            const alertDiv = document.createElement('div');
            alertDiv.className = 'alert alert-info';
            alertDiv.innerHTML = `<strong>ℹ️ Información:</strong> ${resultado.omitidos} archivo(s) omitido(s) (archivos del sistema, comprimidos o ejecutables)`;
            previewContent.appendChild(alertDiv);
        }
        
        if (categorias.length === 0) {
            previewContent.innerHTML += '<p class="help-text">No se encontraron archivos para organizar en esta carpeta.</p>';
            previewCard.style.display = 'block';
            return;
        }
        
        categorias.forEach(categoria => {
            const archivos = preview[categoria];
            const div = document.createElement('div');
            div.className = 'preview-category';
            
            const titulo = document.createElement('h3');
            titulo.textContent = `${categoria} (${archivos.length})`;
            div.appendChild(titulo);
            
            const filesDiv = document.createElement('div');
            filesDiv.className = 'preview-files';
            
            archivos.slice(0, 10).forEach(archivo => {
                const tag = document.createElement('span');
                tag.className = 'file-tag';
                tag.textContent = archivo;
                filesDiv.appendChild(tag);
            });
            
            if (archivos.length > 10) {
                const tag = document.createElement('span');
                tag.className = 'file-tag';
                tag.textContent = `+${archivos.length - 10} más...`;
                tag.style.background = '#e2e8f0';
                filesDiv.appendChild(tag);
            }
            
            div.appendChild(filesDiv);
            previewContent.appendChild(div);
        });
        
        previewCard.style.display = 'block';
        
    } catch (error) {
        mostrarError('Error al obtener vista previa: ' + error);
    }
}

// Actualizar vista previa
async function actualizarVista() {
    // Verificar que hay una ruta establecida
    if (!rutaActual) {
        mostrarError('Por favor, establece una ruta primero haciendo clic en "Establecer"');
        return;
    }
    
    try {
        mostrarLoader(true);
        const resultado = await eel.obtener_vista_previa(rutaActual)();
        mostrarLoader(false);
        
        if (!resultado.success) {
            mostrarError(resultado.mensaje);
            return;
        }
        
        const previewContent = document.getElementById('previewContent');
        previewContent.innerHTML = '';
        
        const preview = resultado.preview;
        const categorias = Object.keys(preview);
        
        // Mostrar información de archivos omitidos
        if (resultado.omitidos > 0) {
            const alertDiv = document.createElement('div');
            alertDiv.className = 'alert alert-info';
            alertDiv.innerHTML = `<strong>ℹ️ Información:</strong> ${resultado.omitidos} archivo(s) omitido(s) (archivos del sistema, comprimidos o ejecutables)`;
            previewContent.appendChild(alertDiv);
        }
        
        if (categorias.length === 0) {
            const alertDiv = document.createElement('div');
            alertDiv.className = 'alert alert-success';
            alertDiv.innerHTML = '<strong>✓ Todo limpio!</strong> No hay archivos nuevos para organizar.';
            previewContent.appendChild(alertDiv);
            return;
        }
        
        categorias.forEach(categoria => {
            const archivos = preview[categoria];
            const div = document.createElement('div');
            div.className = 'preview-category';
            
            const titulo = document.createElement('h3');
            titulo.textContent = `${categoria} (${archivos.length})`;
            div.appendChild(titulo);
            
            const filesDiv = document.createElement('div');
            filesDiv.className = 'preview-files';
            
            archivos.slice(0, 10).forEach(archivo => {
                const tag = document.createElement('span');
                tag.className = 'file-tag';
                tag.textContent = archivo;
                filesDiv.appendChild(tag);
            });
            
            if (archivos.length > 10) {
                const tag = document.createElement('span');
                tag.className = 'file-tag';
                tag.textContent = `+${archivos.length - 10} más...`;
                tag.style.background = '#e2e8f0';
                filesDiv.appendChild(tag);
            }
            
            div.appendChild(filesDiv);
            previewContent.appendChild(div);
        });
        
    } catch (error) {
        mostrarLoader(false);
        mostrarError('Error al actualizar vista: ' + error);
    }
}

// Ejecutar organización
async function ejecutarOrganizacion() {
    if (!rutaActual) {
        mostrarError('Por favor, establece una ruta primero');
        return;
    }
    
    const confirmacion = confirm('¿Estás seguro de que deseas organizar los archivos? Esta acción moverá los archivos a carpetas según su tipo.');
    
    if (!confirmacion) {
        return;
    }
    
    mostrarLoader(true);
    
    try {
        const resultado = await eel.organizar_archivos()();
        
        mostrarLoader(false);
        
        if (!resultado.success) {
            mostrarError(resultado.mensaje);
            return;
        }
        
        mostrarResultados(resultado);
        
    } catch (error) {
        mostrarLoader(false);
        mostrarError('Error al organizar archivos: ' + error);
    }
}

// Mostrar resultados
function mostrarResultados(resultado) {
    const resultadosCard = document.getElementById('resultadosCard');
    const estadisticas = document.getElementById('estadisticas');
    const detalles = document.getElementById('detalles');
    
    // Estadísticas
    const stats = resultado.estadisticas;
    estadisticas.innerHTML = `
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">${stats.movidos}</div>
                <div class="stat-label">Archivos Movidos</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">${stats.errores}</div>
                <div class="stat-label">Errores</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">${stats.omitidos}</div>
                <div class="stat-label">Omitidos</div>
            </div>
        </div>
    `;
    
    // Detalles
    detalles.innerHTML = '<h3 style="margin-bottom: 15px;">Detalles de la Operación</h3>';
    
    const resultados = resultado.resultados;
    const maxMostrar = 50;
    
    resultados.slice(0, maxMostrar).forEach(item => {
        const div = document.createElement('div');
        div.className = `resultado-item ${item.exito ? 'resultado-exito' : 'resultado-error'}`;
        
        div.innerHTML = `
            <span><strong>${item.archivo}</strong> → ${item.categoria}</span>
            <span>${item.exito ? '✓' : '✗'}</span>
        `;
        
        detalles.appendChild(div);
    });
    
    if (resultados.length > maxMostrar) {
        const p = document.createElement('p');
        p.className = 'help-text';
        p.textContent = `... y ${resultados.length - maxMostrar} archivos más`;
        detalles.appendChild(p);
    }
    
    resultadosCard.style.display = 'block';
    
    // Ocultar vista previa
    document.getElementById('previewCard').style.display = 'none';
    
    // Scroll a resultados
    resultadosCard.scrollIntoView({ behavior: 'smooth' });
}

// Mostrar/ocultar loader
function mostrarLoader(mostrar) {
    document.getElementById('loader').style.display = mostrar ? 'flex' : 'none';
}

// Mostrar error
function mostrarError(mensaje) {
    const previewContent = document.getElementById('previewContent');
    previewContent.innerHTML = `
        <div class="alert alert-error">
            <strong>Error:</strong> ${mensaje}
        </div>
    `;
    document.getElementById('previewCard').style.display = 'block';
}

// Permitir edición manual de la ruta
document.getElementById('rutaInput').addEventListener('dblclick', function() {
    this.removeAttribute('readonly');
    this.focus();
});

document.getElementById('rutaInput').addEventListener('blur', function() {
    this.setAttribute('readonly', 'readonly');
});

// Cargar ruta de documentos al iniciar
window.addEventListener('load', () => {
    cargarRutaDocumentos();
});