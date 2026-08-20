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
    if (email && password) {
        document.cookie = `token=mock_jwt_token_12345; path=/; SameSite=Lax`;
        window.location.href = 'index.html';
        return;
    }
    showError('Please fill in all fields.');
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
