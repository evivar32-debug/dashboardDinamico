/**
 * LÓGICA DE CONTROL - DASHBOARD IOT
 * ---------------------------------
 * Gestiona el ciclo de vida de los datos: Fetch -> Procesamiento -> Visualización.
 * Implementa Polling para actualización en tiempo real sin recarga de página.
 */

// --- 1. CONFIGURACIÓN Y SELECTORES ---
const API_BASE_URL = 'http://localhost:8000/api/sensores';
const ctx = document.getElementById('iotChart').getContext('2d');
const menuContainer = document.getElementById('menuDispositivos');
const sensorTitulo = document.getElementById('sensorTitulo');
const statusBadge = document.getElementById('statusBadge');

// Estado global de la aplicación (Sensor actualmente en monitoreo)
window.sensorSeleccionado = null;

// --- 2. INICIALIZACIÓN DEL INSTRUMENTO VIRTUAL (CHART.JS) ---
/**
 * Se inicializa el objeto Chart una sola vez para optimizar RAM.
 * Las actualizaciones posteriores usarán el método .update()
 */
let iotChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [], // Eje X: Timestamps
        datasets: [{
            label: 'Lectura en Tiempo Real',
            data: [], // Eje Y: Valores del sensor
            borderColor: '#03a9f4',
            backgroundColor: 'rgba(3, 169, 244, 0.1)',
            fill: true,
            tension: 0.4,       // Suavizado de curva (Bézier)
            pointRadius: 4,
            pointBackgroundColor: '#03a9f4'
        }]
    },
    options: { 
        responsive: true,
        maintainAspectRatio: false, // Permite que el CSS controle el alto
        plugins: {
            legend: { position: 'top' }
        },
        scales: {
            y: { beginAtZero: false },
            x: { title: { display: true, text: 'Hora de Lectura' } }
        }
    }
});

// --- 3. CONSUMO DE API: CONSTRUCCIÓN DEL MENÚ ---
/**
 * Obtiene la jerarquía de hardware (Placas -> Sensores) desde el backend.
 * Implementa autoselección del primer sensor disponible.
 */
async function cargarMenu() {
    try {
        const response = await fetch(`${API_BASE_URL}/menu/`);
        const dispositivos = await response.json();
        menuContainer.innerHTML = '';

        dispositivos.forEach(disp => {
            const group = document.createElement('div');
            group.className = 'dispositivo-group';
            
            // Etiqueta del Dispositivo (Hardware/Placa)
            const label = document.createElement('div');
            label.className = 'dispositivo-label';
            label.textContent = disp.nombre_placa;
            group.appendChild(label);

            // Mapeo de sensores vinculados a dicha placa
            disp.sensores.forEach(sensor => {
                const item = document.createElement('div');
                item.className = 'sensor-item';
                item.textContent = sensor.nombre;
                // Closure para capturar el estado del sensor al hacer click
                item.onclick = () => seleccionarSensor(sensor.slug, sensor.nombre, item);
                group.appendChild(item);
            });
            menuContainer.appendChild(group);
        });

        // Autoselección inicial para UX (User Experience)
        if (dispositivos.length > 0 && dispositivos[0].sensores.length > 0) {
            const s = dispositivos[0].sensores[0];
            const primerItem = document.querySelector('.sensor-item');
            seleccionarSensor(s.slug, s.nombre, primerItem);
        }
    } catch (error) {
        console.error("Fallo de comunicación con API:", error);
        menuContainer.innerHTML = '<div style="padding:20px; color:#ef5350;">Error de enlace con servidor</div>';
    }
}

// --- 4. GESTIÓN DE EVENTOS Y SELECCIÓN ---
function seleccionarSensor(slug, nombre, elemento) {
    window.sensorSeleccionado = slug;
    
    // Actualización de UI: Feedback visual en menú
    document.querySelectorAll('.sensor-item').forEach(el => el.classList.remove('active'));
    elemento.classList.add('active');
    
    // Actualización de UI: Identificadores de cabecera
    sensorTitulo.textContent = `Sensor: ${nombre}`;
    statusBadge.style.display = 'inline-block';
    
    // Disparo inmediato de la primera lectura
    actualizarDatos();
}

// --- 5. PROCESAMIENTO DE SEÑALES (LECTURAS) ---
/**
 * Función núcleo: Solicita datos, calcula KPIs y actualiza el gráfico.
 * Utiliza decodificación JSON y manejo de arrays para min/max.
 */
async function actualizarDatos() {
    if (!window.sensorSeleccionado) return;
    
    try {
        const url = `${API_BASE_URL}/lecturas/?sensor__slug=${encodeURIComponent(window.sensorSeleccionado)}`;
        const response = await fetch(url);
        const rawData = await response.json();
        
        // Manejo de paginación de Django Rest Framework (DRF) o arrays simples
        const lecturasRaw = Array.isArray(rawData) ? rawData : rawData.results;
        
        if (!lecturasRaw || lecturasRaw.length === 0) return;

        // Invertimos el orden para mostrar la línea de tiempo correctamente (Pasado -> Presente)
        const lecturas = [...lecturasRaw].reverse();

        // Cálculo de KPIs (Key Performance Indicators)
        const ultimo = lecturas[lecturas.length - 1];
        const valores = lecturas.map(l => l.valor);
        
        document.getElementById('lastValue').textContent = `${ultimo.valor}°C`;
        document.getElementById('maxValue').textContent = `${Math.max(...valores)}°C`;
        
        // Actualización de datos en el objeto Chart existente
        iotChart.data.labels = lecturas.map(l => {
            return new Date(l.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
        });
        iotChart.data.datasets[0].data = valores;
        
        // 'none' desactiva animaciones de entrada para ahorrar CPU en monitoreo constante
        iotChart.update('none'); 
        
        renderizarTabla(lecturas);

    } catch (error) {
        console.error("Error en flujo de datos:", error);
        const indicator = document.getElementById('statusIndicator');
        indicator.textContent = "Desconectado";
        indicator.className = "status-offline";
    }
}

// --- 6. RENDERIZADO DE TABLA (LOGS) ---
/**
 * Transforma los datos crudos en filas de tabla HTML.
 * Limita la vista a los últimos 10 eventos para evitar saturación del DOM.
 */
function renderizarTabla(lecturas) {
    const tableBody = document.getElementById('logTableBody');
    tableBody.innerHTML = '';

    // Re-ordenamos para mostrar lo más nuevo arriba en la tabla (LIFO)
    const ultimasDiez = [...lecturas].reverse().slice(0, 10);

    ultimasDiez.forEach(l => {
        const row = document.createElement('tr');
        const fecha = new Date(l.timestamp).toLocaleString();
        
        row.innerHTML = `
            <td>${fecha}</td>
            <td>${l.tipo}</td>
            <td><strong>${l.valor}</strong></td>
            <td><span class="tag-success">RECIBIDO</span></td>
        `;
        tableBody.appendChild(row);
    });
}

// --- 7. INICIO Y CICLO DE VIDA ---
cargarMenu();

/**
 * Polling (Muestreo): Ejecuta la actualización cada 10 segundos.
 * Equivalente industrial al tiempo de escaneo de un PLC para variables lentas (Temp).
 */
setInterval(() => {
    if (window.sensorSeleccionado) actualizarDatos();
}, 10000);