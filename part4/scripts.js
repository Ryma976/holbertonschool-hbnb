document.addEventListener('DOMContentLoaded', () => {
    // Task 1: Login Form Handler
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

    // Task 2: Index Page Handler
    const placesList = document.getElementById('places-list');
    if (placesList) {
        checkAuthentication();
    }
});

// Helper: Get Cookie
function getCookie(name) {
    const nameEQ = name + "=";
    const ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

// Task 1: Login Functionality
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

// Task 2: Authentication Check & Data Fetching
function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (!token) {
        if (loginLink) loginLink.style.display = 'block';
    } else {
        if (loginLink) loginLink.style.display = 'none';
    }
    fetchPlaces(token);
}

let allPlacesData = [];

async function fetchPlaces(token) {
    const headers = {
        'Content-Type': 'application/json'
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/places', { headers });
        if (response.ok) {
            allPlacesData = await response.json();
            displayPlaces(allPlacesData);
            setupPriceFilter();
        } else {
            console.error('Failed to fetch places:', response.statusText);
        }
    } catch (error) {
        console.error('Error fetching places:', error);
    }
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;

    placesList.innerHTML = '';

    places.forEach(place => {
        const placeDiv = document.createElement('div');
        placeDiv.className = 'place-card';
        placeDiv.setAttribute('data-price', place.price_by_night || place.price || 0);

        placeDiv.innerHTML = `
            <h3>${place.title || place.name}</h3>
            <p><strong>Price per night:</strong> $${place.price_by_night || place.price}</p>
            <p>${place.description || 'No description available.'}</p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;

        placesList.appendChild(placeDiv);
    });
}

function setupPriceFilter() {
    const priceFilter = document.getElementById('price-filter');
    if (!priceFilter) return;

    priceFilter.addEventListener('change', (event) => {
        const selectedValue = event.target.value;
        const placeCards = document.querySelectorAll('#places-list .place-card');

        placeCards.forEach(card => {
            const cardPrice = parseFloat(card.getAttribute('data-price'));

            if (selectedValue === 'All' || selectedValue === 'all' || selectedValue === '') {
                card.style.display = 'block';
            } else {
                const maxPrice = parseFloat(selectedValue);
                if (cardPrice <= maxPrice) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            }
        });
    });
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
