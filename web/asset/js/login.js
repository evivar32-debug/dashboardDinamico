document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const errorMsg = document.getElementById('error-msg');

    try {
        const response = await fetch('http://localhost:8000/api/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
            // Guardamos tokens y datos básicos del usuario
            localStorage.setItem('accessToken', data.access);
            localStorage.setItem('refreshToken', data.refresh);
            localStorage.setItem('userName', data.user.nombre);
            localStorage.setItem('is_admin', data.user.es_admin);
            
            // Redirección al Dashboard
            window.location.href = 'asset/page/menu.html';
        } else {
            errorMsg.style.display = 'block';
            errorMsg.textContent = "Error: " + (data.detail || "Credenciales inválidas");
        }
    } catch (error) {
        console.error("Error en el login:", error);
        errorMsg.style.display = 'block';
        errorMsg.textContent = "No se pudo conectar con el servidor.";
    }
});