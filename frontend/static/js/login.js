document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const errorAlert = document.getElementById('errorAlert');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const submitBtn = document.getElementById('submitBtn');

    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        // Validación del formulario
        if (!loginForm.checkValidity()) {
            e.stopPropagation();
            loginForm.classList.add('was-validated');
            return;
        }

        // Obtener los valores del formulario
        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value;

        if (!username || !password) {
            errorAlert.textContent = 'Por favor completa todos los campos';
            errorAlert.classList.remove('d-none');
            return;
        }

        // Mostrar spinner y deshabilitar botón
        loadingSpinner.classList.remove('d-none');
        submitBtn.disabled = true;
        errorAlert.classList.add('d-none');

        try {
            const response = await fetch('http://localhost:5000/api/v1/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();

            if (response.ok) {
                // Guardar el token y la información del usuario
                localStorage.setItem('access_token', data.access_token);
                localStorage.setItem('user', JSON.stringify(data.user));
                
                // Redirigir al usuario a la página principal
                window.location.href = '/cuenta';
            } else {
                // Mostrar mensaje de error específico
                errorAlert.textContent = data.error || 'Error al iniciar sesión';
                errorAlert.classList.remove('d-none');
            }
        } catch (error) {
            console.error('Error:', error);
            errorAlert.textContent = 'Error al iniciar sesión';
            errorAlert.classList.remove('d-none');
        } finally {
            // Ocultar spinner y habilitar botón
            loadingSpinner.classList.add('d-none');
            submitBtn.disabled = false;
        }
    });

    // Ocultar mensaje de error cuando el usuario empiece a escribir
    loginForm.addEventListener('input', function() {
        errorAlert.classList.add('d-none');
    });
});