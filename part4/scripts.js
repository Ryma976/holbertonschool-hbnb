document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            await loginUser(email, password);
        });
    }
});

async function loginUser(email, password) {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        if (response.ok) {
            const data = await response.json();
            
            // حفظ الـ JWT token في الكوكي
            document.cookie = `token=${data.access_token}; path=/; max-age=86400`;

            // التوجيه للصفحة الرئيسية
            window.location.href = 'index.html';
        } else {
            const errorData = await response.json().catch(() => ({}));
            alert('Login failed: ' + (errorData.message || response.statusText));
        }
    } catch (error) {
        console.error('Error during login:', error);
        alert('Could not connect to server. Please ensure the backend server is running.');
    }
}
