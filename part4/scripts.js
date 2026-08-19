document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication();

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
}

async function fetchPlaces() {
    try {
        const response = await fetch('/api/v1/places');
        if (response.ok) {
            const places = await response.json();
            displayPlaces(places);
        } else {
            useMockData();
        }
    } catch (error) {
        useMockData();
    }
}

function useMockData() {
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
