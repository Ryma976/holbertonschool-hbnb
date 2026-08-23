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
        checkAdminPrivileges();
    }

    // Task 3: Place Details Page Handler
    const placeDetails = document.getElementById('place-details');
    if (placeDetails) {
        initPlaceDetailsPage();
    }

    // Task 4: Add Review Form Handler
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        initAddReviewPage(reviewForm);
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

// Task 1: Login Functionality (Mock Login & Admin Detection)
async function loginUser(email, password) {
    if (email && password) {
        const isAdmin = (email === 'admin@hbnb.io');
        
        document.cookie = `token=mock_jwt_token_12345; path=/; SameSite=Lax`;
        document.cookie = `is_admin=${isAdmin}; path=/; SameSite=Lax`;
        
        window.location.href = 'index.html';
        return;
    }
    showError('Please fill in all fields.');
}

// Admin Panel Check
function checkAdminPrivileges() {
    const isAdminCookie = getCookie('is_admin');
    
    if (isAdminCookie === 'true') {
        let adminPanel = document.getElementById('admin-panel');
        if (!adminPanel) {
            const div = document.createElement('div');
            div.id = 'admin-panel';
            div.style.background = '#f8d7da';
            div.style.padding = '12px';
            div.style.textAlign = 'center';
            div.style.fontWeight = 'bold';
            div.style.color = '#721c24';
            div.style.margin = '10px 0';
            div.innerHTML = `⚠️ Admin Mode Active: You have full administrator privileges. <button onclick="alert('Admin privileges: You can manage places and amenities.')" style="margin-left: 10px; padding: 5px 10px; cursor: pointer;">Admin Panel</button>`;
            
            const main = document.querySelector('main') || document.body;
            main.insertBefore(div, main.firstChild);
        }
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
    const headers = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = `Bearer ${token}`;

    try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/places', { headers });
        if (response.ok) {
            allPlacesData = await response.json();
            displayPlaces(allPlacesData);
            setupPriceFilter();
        } else {
            console.error('Failed to fetch places, using mock data.');
            loadMockPlaces();
        }
    } catch (error) {
        console.error('Error fetching places, using mock data:', error);
        loadMockPlaces();
    }
}

// Mock data fallback if server is offline
function loadMockPlaces() {
    allPlacesData = [
        { id: '1', title: 'Cozy Apartment', price: 80, description: 'A nice cozy apartment in downtown.', amenities: ['WiFi', 'Kitchen'] },
        { id: '2', title: 'Luxury Villa', price: 250, description: 'A beautiful luxury villa with a pool.', amenities: ['Pool', 'WiFi', 'AC'] }
    ];
    displayPlaces(allPlacesData);
    setupPriceFilter();
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

// Task 3: Place Details & Reviews
function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

async function initPlaceDetailsPage() {
    const token = getCookie('token');
    const placeId = getPlaceIdFromURL();

    const addReviewSection = document.getElementById('add-review');
    if (addReviewSection) {
        if (!token) {
            addReviewSection.style.display = 'none';
        } else {
            addReviewSection.style.display = 'block';
            const addReviewLink = addReviewSection.querySelector('a');
            if (addReviewLink && placeId) {
                addReviewLink.href = `add_review.html?id=${placeId}`;
            }
        }
    }

    if (placeId) {
        await fetchPlaceDetails(token, placeId);
    }
}

async function fetchPlaceDetails(token, placeId) {
    const headers = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = `Bearer ${token}`;

    try {
        const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, { headers });
        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place);
        } else {
            loadMockPlaceDetails(placeId);
        }
    } catch (error) {
        loadMockPlaceDetails(placeId);
    }
}

function loadMockPlaceDetails(placeId) {
    const found = allPlacesData.find(p => p.id === placeId) || {
        title: 'Sample Place',
        price: 100,
        description: 'Detailed description of the sample place.',
        amenities: ['WiFi']
    };
    displayPlaceDetails(found);
}

function displayPlaceDetails(place) {
    const placeDetails = document.getElementById('place-details');
    if (!placeDetails) return;

    const hostName = place.host_name || (place.user ? `${place.user.first_name} ${place.user.last_name}` : 'Admin Host');
    const amenitiesList = place.amenities ? place.amenities.map(a => a.name || a).join(', ') : 'None';

    placeDetails.innerHTML = `
        <h1>${place.title || place.name}</h1>
        <p><strong>Host:</strong> ${hostName}</p>
        <p><strong>Price per night:</strong> $${place.price_by_night || place.price}</p>
        <p><strong>Description:</strong> ${place.description || 'No description provided.'}</p>
        <p><strong>Amenities:</strong> ${amenitiesList}</p>
    `;

    if (place.reviews) {
        displayReviews(place.reviews);
    }
}

function displayReviews(reviews) {
    const reviewsSection = document.getElementById('reviews');
    if (!reviewsSection) return;

    reviewsSection.innerHTML = '<h2>Reviews</h2>';

    if (!reviews || reviews.length === 0) {
        reviewsSection.innerHTML += '<p>No reviews yet.</p>';
        return;
    }

    reviews.forEach(review => {
        const reviewDiv = document.createElement('div');
        reviewDiv.className = 'review-card';
        reviewDiv.style.border = '1px solid #ddd';
        reviewDiv.style.borderRadius = '5px';
        reviewDiv.style.margin = '10px 0';
        reviewDiv.style.padding = '10px';

        const userName = review.user_name || (review.user ? `${review.user.first_name}` : 'User');

        reviewDiv.innerHTML = `
            <p><strong>${userName}:</strong> ${review.text || review.comment}</p>
            <p><strong>Rating:</strong> ${review.rating || 'N/A'}/5</p>
        `;
        reviewsSection.appendChild(reviewDiv);
    });
}

// Task 4: Add Review Functionality
function initAddReviewPage(reviewForm) {
    const token = getCookie('token');
    if (!token) {
        window.location.href = 'index.html';
        return;
    }

    const placeId = getPlaceIdFromURL();

    reviewForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const reviewTextInput = document.getElementById('review-text') || document.getElementById('review') || document.getElementById('comment');
        const ratingInput = document.getElementById('rating');

        const reviewText = reviewTextInput ? reviewTextInput.value.trim() : '';
        const rating = ratingInput ? parseInt(ratingInput.value, 10) : 5;

        if (!reviewText) {
            alert('Please write a review.');
            return;
        }

        alert('Review submitted successfully (Mock Mode)!');
        window.location.href = placeId ? `place.html?id=${placeId}` : 'index.html';
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
