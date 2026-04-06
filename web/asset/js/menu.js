/**
 * LÓGICA DE CONTROL - DASHBOARD IOT
 * ---------------------------------
 */

// --- CONTROL DE ACCESO ---
if (!localStorage.getItem('accessToken')) {
    window.location.href = '../../index.html';
}

document.addEventListener('DOMContentLoaded', () => {
    const userName = localStorage.getItem('userName');
    const isAdmin = localStorage.getItem('is_admin') === 'true'; // Capturamos el rol
    const displayEl = document.getElementById('displayUserName');

    if (displayEl && userName) {
        // 1. Mostrar nombre y Badge de Rol
        const rol = isAdmin ? 'ADMINISTRADOR' : 'OPERADOR';
        displayEl.innerHTML = `
            <div class="user-info">
                <span class="user-name">${userName}</span>
                <span class="user-role ${isAdmin ? 'role-admin' : 'role-worker'}">${rol}</span>
            </div>
        `;
    }

    // 2. Inyectar botón de Agregar SENSOR solo si es Admin
    if (isAdmin) {
        const adminPanel = document.querySelector('.admin-controls');
        if (adminPanel) {
            adminPanel.innerHTML = `
                <button onclick="abrirModalSensor()" class="btn-add-sensor">
                    <i class="fas fa-plus"></i> AGREGAR SENSOR
                </button>
            `;
        }

        // Inicializar el escuchador del formulario del modal
        const form = document.getElementById('formNuevoSensor');
        if (form) form.onsubmit = guardarSensorAPI;
    }

    // 3. Gestión de Logout
    const btnLogout = document.getElementById('btnLogout');
    if (btnLogout) {
        btnLogout.onclick = () => {
            localStorage.clear();
            window.location.href = '../../index.html';
        };
    }

    // 4. Autogeneración de Slug
    const inputNombre = document.getElementById('nombreSensor');
    const inputSlug = document.getElementById('slugSensor');

    if (inputNombre && inputSlug) {
        inputNombre.addEventListener('input', () => {
            // Solo autogenerar si el usuario no ha escrito manualmente en el slug
            // o si el slug está vacío.
            inputSlug.value = generarSlug(inputNombre.value);
        });
    }
});

// --- 1. CONFIGURACIÓN Y SELECTORES ---
const API_BASE_URL = 'http://localhost:8000/api/sensores';
const ctx = document.getElementById('iotChart').getContext('2d');
const menuContainer = document.getElementById('menuDispositivos');
const sensorTitulo = document.getElementById('sensorTitulo');
const statusBadge = document.getElementById('statusBadge');

window.sensorSeleccionado = null;

// --- 2. INICIALIZACIÓN DEL GRÁFICO (CHART.JS) ---
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
        maintainAspectRatio: false,
        scales: { y: { beginAtZero: false } }
    }
});

// --- 3. LÓGICA DE MODAL (NUEVO) ---

window.abrirModalSensor = function () {
    const modal = document.getElementById('modalSensor');
    if (modal) {
        modal.style.display = 'flex';
        cargarDispositivosEnSelect();
    }
};

window.cerrarModal = function () {
    const modal = document.getElementById('modalSensor');
    if (modal) modal.style.display = 'none';
};

async function cargarDispositivosEnSelect() {
    const token = localStorage.getItem('accessToken');
    const select = document.getElementById('selectDispositivo');
    if (!select) return;

    try {
        const response = await fetch(`${API_BASE_URL}/menu/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const dispositivos = await response.json();

        // Limpieza y llenado
        select.innerHTML = '<option value="" disabled selected>Seleccione la placa base...</option>';
        
        dispositivos.forEach(p => {
            const option = document.createElement('option');
            // IMPORTANTE: p.id es el que requiere la ForeignKey en el modelo Sensor
            option.value = p.id; 
            option.textContent = `${p.nombre_placa} (${p.chip_id})`;
            select.appendChild(option);
        });
    } catch (err) {
        console.error("Error cargando dispositivos:", err);
    }
}

async function guardarSensorAPI(e) {
    e.preventDefault();
    const token = localStorage.getItem('accessToken');
    
    // Captura del ID de la placa
    const idPlaca = document.getElementById('selectDispositivo').value;

    const datos = {
        dispositivo: parseInt(idPlaca), // El ID numérico que vincula a la ForeignKey
        nombre: document.getElementById('nombreSensor').value,
        slug: document.getElementById('slugSensor').value,
        pin_conexion: parseInt(document.getElementById('pinConexion').value),
        tipo: document.getElementById('tipoSensor').value
    };

    try {
        const response = await fetch(`${API_BASE_URL}/`, { // O /lista/ según tu urls.py
            method: 'POST',
            headers: { 
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json' 
            },
            body: JSON.stringify(datos)
        });

        if (response.ok) {
            cerrarModal();
            alert("Sensor vinculado exitosamente al hardware.");
            cargarMenu(); 
        } else {
            const errorData = await response.json();
            console.error("Fallo de validación en Django:", errorData);
            alert("Error: " + JSON.stringify(errorData));
        }
    } catch (err) {
        console.error("Error de red:", err);
    }
}

// --- 4. CONSUMO DE API: MENÚ Y DATOS (Tu lógica original intacta) ---
async function cargarMenu() {
    const token = localStorage.getItem('accessToken');
    try {
        const response = await fetch(`${API_BASE_URL}/menu/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (response.status === 401) return document.getElementById('btnLogout').click();

        const dispositivos = await response.json();
        menuContainer.innerHTML = '';

        dispositivos.forEach(disp => {
            const group = document.createElement('div');
            group.className = 'dispositivo-group';
            group.innerHTML = `<div class="dispositivo-label">${disp.nombre_placa}</div>`;

            disp.sensores.forEach(sensor => {
                const item = document.createElement('div');
                item.className = 'sensor-item';
                item.textContent = sensor.nombre;
                item.onclick = () => seleccionarSensor(sensor.slug, sensor.nombre, item);
                group.appendChild(item);
            });
            menuContainer.appendChild(group);
        });

        if (dispositivos.length > 0 && dispositivos[0].sensores.length > 0) {
            const s = dispositivos[0].sensores[0];
            const primerItem = document.querySelector('.sensor-item');
            if (primerItem) seleccionarSensor(s.slug, s.nombre, primerItem);
        }
    } catch (error) { console.error("Fallo de comunicación:", error); }
}

function seleccionarSensor(slug, nombre, elemento) {
    window.sensorSeleccionado = slug;
    document.querySelectorAll('.sensor-item').forEach(el => el.classList.remove('active'));
    elemento.classList.add('active');
    sensorTitulo.textContent = `Sensor: ${nombre}`;
    statusBadge.style.display = 'inline-block';
    actualizarDatos();
}

async function actualizarDatos() {
    if (!window.sensorSeleccionado) return;
    const token = localStorage.getItem('accessToken');
    try {
        const url = `${API_BASE_URL}/lecturas/?sensor__slug=${encodeURIComponent(window.sensorSeleccionado)}`;
        const response = await fetch(url, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        const rawData = await response.json();
        const lecturas = Array.isArray(rawData) ? rawData : rawData.results;
        if (!lecturas || lecturas.length === 0) return;

        const dataRev = [...lecturas].reverse();
        const ultimo = dataRev[dataRev.length - 1];
        const valores = dataRev.map(l => l.valor);

        document.getElementById('lastValue').textContent = `${ultimo.valor}°C`;
        document.getElementById('maxValue').textContent = `${Math.max(...valores)}°C`;

        iotChart.data.labels = dataRev.map(l => new Date(l.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }));
        iotChart.data.datasets[0].data = valores;
        iotChart.update('none');

        renderizarTabla(dataRev);
    } catch (error) { console.error("Error en flujo de datos:", error); }
}

function renderizarTabla(lecturas) {
    const tableBody = document.getElementById('logTableBody');
    tableBody.innerHTML = '';
    [...lecturas].reverse().slice(0, 10).forEach(l => {
        tableBody.innerHTML += `
            <tr>
                <td>${new Date(l.timestamp).toLocaleString()}</td>
                <td>${l.tipo}</td>
                <td><strong>${l.valor}</strong></td>
                <td><span class="tag-success">RECIBIDO</span></td>
            </tr>`;
    });
}

/**
 * Transforma una cadena de texto en un slug válido para Django.
 * Ejemplo: "Presión Caldera 01" -> "presion-caldera-01"
 */
function generarSlug(texto) {
    return texto
        .toString()                     // Asegurar que sea string
        .toLowerCase()                  // Todo a minúsculas
        .trim()                         // Quitar espacios extremos
        .normalize('NFD')               // Descomponer caracteres acentuados
        .replace(/[\u0300-\u036f]/g, '') // Eliminar las tildes
        .replace(/\s+/g, '_')           // Reemplazar espacios por guiones bajos
        .replace(/[^\w\-]+/g, '')       // Eliminar caracteres especiales
        .replace(/\-\-+/g, '_');        // Evitar guiones bajos dobles
}

// --- 5. CICLO DE VIDA ---
cargarMenu();
setInterval(() => {
    if (window.sensorSeleccionado) actualizarDatos();
}, 10000);