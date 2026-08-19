document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication();

    // إعداد نموذج تسجيل الدخول (Task 1)
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            await loginUser(email, password);
        });
    }

    // إعداد تصفية الأسعار (Task 2)
    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.addEventListener('change', (event) => {
            const selectedValue = event.target.value;
            const placeCards = document.querySelectorAll('#places-list .place-card');

            placeCards.forEach(card => {
                const cardPrice = parseFloat(card.dataset.price);
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
});

// دالة جلب قيمة الكوكي باسمها
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// دالة التحقق من تسجيل الدخول
function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (loginLink) {
        if (!token) {
            loginLink.style.display = 'inline-block';
        } else {
            loginLink.style.display = 'none';
        }
    }

    if (document.getElementById('places-list')) {
        fetchPlaces(token);
    }
}

// دالة تسجيل الدخول
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
            const errorData = await response.json().catch(() => ({}));
            alert('Login failed: ' + (errorData.message || response.statusText));
        }
    } catch (error) {
        console.error('Error during login:', error);
        alert('Could not connect to server. Ensure server is running.');
    }
}

// دالة جلب الأماكن من API
async function fetchPlaces(token) {
    try {
        const headers = { 'Content-Type': 'application/json' };
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch('/api/v1/places', {
            method: 'GET',
            headers: headers
        });

        if (response.ok) {
            const places = await response.json();
            displayPlaces(places);
        } else {
            console.error('Failed to fetch places:', response.statusText);
        }
    } catch (error) {
        console.error('Error fetching places:', error);
    }
}

// دالة عرض الأماكن ديناميكياً
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
