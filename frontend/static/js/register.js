document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.getElementById('registerForm');
    const errorAlert = document.getElementById('errorAlert');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const submitBtn = document.getElementById('submitBtn');

    registerForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Validación del formulario
        if (!registerForm.checkValidity()) {
            e.stopPropagation();
            registerForm.classList.add('was-validated');
            return;
        }

        // Obtener los valores del formulario
        const name = document.getElementById('name').value.trim();
        const username = document.getElementById('username').value.trim();
        const phone = document.getElementById('phone').value.trim();
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirm-password').value;

        // Validaciones adicionales
        if (!name || !username || !phone || !password || !confirmPassword) {
            errorAlert.textContent = 'Por favor completa todos los campos';
            errorAlert.classList.remove('d-none');
            return;
        }

        // Validar que las contraseñas coincidan
        if (password !== confirmPassword) {
            errorAlert.textContent = 'Las contraseñas no coinciden';
            errorAlert.classList.remove('d-none');
            return;
        }

        // Mostrar spinner y deshabilitar botón
        loadingSpinner.classList.remove('d-none');
        submitBtn.disabled = true;
        errorAlert.classList.add('d-none');

        try {
            const response = await fetch('http://localhost:5000/api/v1/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({ 
                    name, 
                    username, 
                    phone, 
                    password 
                })
            });

            const data = await response.json();

            if (response.ok) {
                // Redirigir al usuario a la página de login o dashboard
                window.location.href = '/login';
            } else {
                // Mostrar mensaje de error específico
                errorAlert.textContent = data.error || 'Error al registrar usuario';
                errorAlert.classList.remove('d-none');
            }
        } catch (error) {
            console.error('Error:', error);
            errorAlert.textContent = 'Error de conexión con el servidor';
            errorAlert.classList.remove('d-none');
        } finally {
            // Ocultar spinner y habilitar botón
            loadingSpinner.classList.add('d-none');
            submitBtn.disabled = false;
        }
    });

    // Ocultar mensaje de error cuando el usuario empiece a escribir
    registerForm.addEventListener('input', function() {
        errorAlert.classList.add('d-none');
    });
});