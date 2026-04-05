/**
 * LÓGICA DE CONTROL - DASHBOARD IOT
 * ---------------------------------
 * Gestiona el ciclo de vida de los datos: Fetch -> Procesamiento -> Visualización.
 * Implementa Polling para actualización en tiempo real sin recarga de página.
 */


// --- CONTROL DE ACCESO ---

/**
 *  Verificación de Seguridad
 * Si no hay token, aborta la carga y redirige al login.
 */
if (!localStorage.getItem('accessToken')) {
    window.location.href = '../../index.html';
}

document.addEventListener('DOMContentLoaded', () => {
    // 2. Mostrar datos del Operador
    const userName = localStorage.getItem('userName');
    const displayEl = document.getElementById('displayUserName');
    if (displayEl && userName) {
        displayEl.textContent = `Operador: ${userName}`;
    }

    // 3. Gestión de Logout
    const btnLogout = document.getElementById('btnLogout');
    if (btnLogout) {
        btnLogout.onclick = () => {
            // Limpieza de memoria local
            localStorage.removeItem('accessToken');
            localStorage.removeItem('refreshToken');
            localStorage.removeItem('userName');
            localStorage.removeItem('is_admin');
            
            // Redirección segura
            window.location.href = '../../index.html';
        };
    }
});

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
    // 1. Recuperamos el token del almacenamiento local
    const token = localStorage.getItem('accessToken');
    
    try {
        const response = await fetch(`${API_BASE_URL}/menu/`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`, // Enviamos el "Gafete" digital
                'Content-Type': 'application/json'
            }
        });

        // 2. Manejo de seguridad: Si el token no es válido o expiró
        if (response.status === 401) {
            console.warn("Sesión expirada o no autorizada.");
            // Forzamos el logout usando el botón que creamos antes
            document.getElementById('btnLogout').click();
            return;
        }

        if (!response.ok) throw new Error('Fallo en la respuesta del servidor');

        const dispositivos = await response.json();
        menuContainer.innerHTML = '';

        dispositivos.forEach(disp => {
            const group = document.createElement('div');
            group.className = 'dispositivo-group';
            
            const label = document.createElement('div');
            label.className = 'dispositivo-label';
            label.textContent = disp.nombre_placa;
            group.appendChild(label);

            disp.sensores.forEach(sensor => {
                const item = document.createElement('div');
                item.className = 'sensor-item';
                item.textContent = sensor.nombre;
                item.onclick = () => seleccionarSensor(sensor.slug, sensor.nombre, item);
                group.appendChild(item);
            });
            menuContainer.appendChild(group);
        });

        // Autoselección inicial
        if (dispositivos.length > 0 && dispositivos[0].sensores.length > 0) {
            const s = dispositivos[0].sensores[0];
            const primerItem = document.querySelector('.sensor-item');
            if (primerItem) seleccionarSensor(s.slug, s.nombre, primerItem);
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
    
    // 1. Recuperamos el token para la petición de datos
    const token = localStorage.getItem('accessToken');
    
    try {
        const url = `${API_BASE_URL}/lecturas/?sensor__slug=${encodeURIComponent(window.sensorSeleccionado)}`;
        
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`, // Autorización requerida por DRF
                'Content-Type': 'application/json'
            }
        });

        // 2. Control de expiración de sesión (401 Unauthorized)
        if (response.status === 401) {
            console.error("Sesión de monitoreo finalizada por seguridad.");
            document.getElementById('btnLogout').click();
            return;
        }

        if (!response.ok) throw new Error('Error en la respuesta de la API');

        const rawData = await response.json();
        const lecturasRaw = Array.isArray(rawData) ? rawData : rawData.results;
        
        if (!lecturasRaw || lecturasRaw.length === 0) return;

        const lecturas = [...lecturasRaw].reverse();

        // 3. Actualización de UI y KPIs
        const ultimo = lecturas[lecturas.length - 1];
        const valores = lecturas.map(l => l.valor);
        
        document.getElementById('lastValue').textContent = `${ultimo.valor}°C`;
        document.getElementById('maxValue').textContent = `${Math.max(...valores)}°C`;
        
        // 4. Actualización del Gráfico (Chart.js)
        iotChart.data.labels = lecturas.map(l => {
            return new Date(l.timestamp).toLocaleTimeString([], { 
                hour: '2-digit', 
                minute: '2-digit', 
                second: '2-digit' 
            });
        });
        iotChart.data.datasets[0].data = valores;
        
        iotChart.update('none'); 
        
        renderizarTabla(lecturas);

    } catch (error) {
        console.error("Error en flujo de datos:", error);
        const indicator = document.getElementById('statusIndicator');
        if (indicator) {
            indicator.textContent = "Error de Enlace";
            indicator.className = "status-offline";
        }
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