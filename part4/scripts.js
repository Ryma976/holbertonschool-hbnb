document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const emailInput = document.getElementById('email');
            const passwordInput = document.getElementById('password');

            const email = emailInput ? emailInput.value.trim() : '';
            const password = passwordInput ? passwordInput.value : '';

            if (!email || !password) {
                showError('Please fill in all fields.');
                return;
            }

            await loginUser(email, password);
        });
    }
});

async function loginUser(email, password) {
    const apiUrl = 'http://127.0.0.1:5000/api/v1/login'; 

    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        if (response.ok) {
            const data = await response.json();
            const token = data.access_token || data.token;
            document.cookie = `token=${token}; path=/; SameSite=Lax`;
            window.location.href = 'index.html';
        } else {
            const errorData = await response.json().catch(() => null);
            const errorMessage = errorData?.msg || errorData?.message || response.statusText;
            showError('Login failed: ' + errorMessage);
        }
    } catch (error) {
        console.error('Error during login:', error);
        showError('Network error. Please check your API connection.');
    }
}

function showError(message) {
    let errorDiv = document.getElementById('error-message');
    if (!errorDiv) {
        errorDiv = document.createElement('div');
        errorDiv.id = 'error-message';
        errorDiv.style.color = '#d9534f';
        errorDiv.style.marginTop = '10px';
        errorDiv.style.textAlign = 'center';
        errorDiv.style.fontWeight = 'bold';
        
        const form = document.getElementById('login-form');
        if (form) form.appendChild(errorDiv);
    }
    errorDiv.textContent = message;
}
