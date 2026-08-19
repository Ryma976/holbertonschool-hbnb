document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication();

    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            await loginUser(email, password);
        });
    }

    if (document.getElementById('places-list')) {
        fetchPlaces();
    }
});

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    if (loginLink) {
        loginLink.style.display = token ? 'none' : 'inline-block';
    }
    return token;
}

async function loginUser(email, password) {
    try {
        const response = await fetch('/api/v1/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        if (response.ok) {
            const data = await response.json();
            document.cookie = `token=${data.access_token}; path=/; max-age=86400`;
            window.location.href = 'index.html';
        } else {
            // محاكاة تسجيل الدخول للعمل على GitHub Pages مباشرة
            if (email === 'admin@hbnb.io' && password === 'admin123') {
                document.cookie = `token=mock_jwt_token_12345; path=/; max-age=86400`;
                alert('Login successful!');
                window.location.href = 'index.html';
            } else {
                alert('Login failed: Invalid credentials');
            }
        }
    } catch (error) {
        // Fallback في حال حظر المتصفح للاتصال بالباك إند Local
        if (email === 'admin@hbnb.io' && password === 'admin123') {
            document.cookie = `token=mock_jwt_token_12345; path=/; max-age=86400`;
            alert('Login successful!');
            window.location.href = 'index.html';
        } else {
            alert('Login failed: Invalid email or password');
        }
    }
}

async function fetchPlaces() {
    try {
        const response = await fetch('/api/v1/places');
        if (response.ok) {
            const places = await response.json();
            displayPlaces(places);
        } else {
            useMockPlaces();
        }
    } catch (error) {
        useMockPlaces();
    }
}

function useMockPlaces() {
    const mockPlaces = [
        { id: "1", title: "Cozy Apartment", price: 45, description: "A nice and cozy apartment in the city center." },
        { id: "2", title: "Luxury Villa", price: 120, description: "Beautiful villa with a private pool and beach view." },
        { id: "3", title: "Studio Room", price: 30, description: "Affordable studio perfect for solo travelers." }
    ];
    displayPlaces(mockPlaces);
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;
    placesList.innerHTML = '';

    places.forEach(place => {
        const price = place.price_by_night || place.price || 0;
        const card = document.createElement('div');
        card.className = 'place-card';
        card.dataset.price = price;

        card.innerHTML = `
            <h2>${place.title || place.name}</h2>
            <p class="price">$${price} per night</p>
            <p class="description">${place.description || ''}</p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;
        placesList.appendChild(card);
    });
}
