// Configuración global
const API_BASE_URL = 'http://localhost:8000/api/sensores';
const ctx = document.getElementById('iotChart').getContext('2d');
const menuContainer = document.getElementById('menuDispositivos');
const sensorTitulo = document.getElementById('sensorTitulo');
const statusBadge = document.getElementById('statusBadge');

window.sensorSeleccionado = null;

// Inicialización del Gráfico
let iotChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Lectura en Tiempo Real',
            data: [],
            borderColor: '#03a9f4',
            backgroundColor: 'rgba(3, 169, 244, 0.1)',
            fill: true,
            tension: 0.4,
            pointRadius: 4,
            pointBackgroundColor: '#03a9f4'
        }]
    },
    options: { 
        responsive: true,
        plugins: {
            legend: { position: 'top' }
        },
        scales: {
            y: { beginAtZero: false },
            x: { title: { display: true, text: 'Hora de Lectura' } }
        }
    }
});

// 1. CARGAR MENÚ DESDE LA API
async function cargarMenu() {
    try {
        const response = await fetch(`${API_BASE_URL}/menu/`);
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

        // Autoselección del primer sensor disponible
        if (dispositivos.length > 0 && dispositivos[0].sensores.length > 0) {
            const s = dispositivos[0].sensores[0];
            const primerItem = document.querySelector('.sensor-item');
            seleccionarSensor(s.slug, s.nombre, primerItem);
        }
    } catch (error) {
        console.error("Error al cargar el menú:", error);
        menuContainer.innerHTML = '<div style="padding:20px; color:#ef5350;">Error de conexión</div>';
    }
}

// 2. GESTIÓN DE SELECCIÓN
function seleccionarSensor(slug, nombre, elemento) {
    window.sensorSeleccionado = slug;
    
    // UI: Clase activa
    document.querySelectorAll('.sensor-item').forEach(el => el.classList.remove('active'));
    elemento.classList.add('active');
    
    // UI: Títulos
    sensorTitulo.textContent = `Sensor: ${nombre}`;
    statusBadge.style.display = 'inline-block';
    
    actualizarDatos();
}

// 3. OBTENER LECTURAS
async function actualizarDatos() {
    if (!window.sensorSeleccionado) return;
    
    try {
        const url = `${API_BASE_URL}/lecturas/?sensor_nombre=${encodeURIComponent(window.sensorSeleccionado)}`;
        const response = await fetch(url);
        const data = await response.json();

        // Invertimos para que el tiempo fluya de izquierda a derecha
        const lecturas = data.reverse();

        iotChart.data.labels = lecturas.map(l => {
            const fecha = new Date(l.timestamp);
            return fecha.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        });

        iotChart.data.datasets[0].data = lecturas.map(l => l.valor);
        iotChart.update('none'); // Update sin animación para mayor fluidez
    } catch (error) {
        console.error("Error al obtener datos:", error);
    }
}

// Ejecución inicial
cargarMenu();

// Refresco automático (Polling) cada 10 segundos
setInterval(() => {
    if (window.sensorSeleccionado) actualizarDatos();
}, 10000);