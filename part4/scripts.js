document.addEventListener('DOMContentLoaded', () => {
    const isAddReviewPage = window.location.pathname.endsWith('add_review.html');
    const token = checkAuthentication(isAddReviewPage);

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

    // إعداد صفحة التفاصيل (Task 3)
    if (document.getElementById('place-details')) {
        const placeId = getPlaceIdFromURL();
        if (placeId) {
            fetchPlaceDetails(token, placeId);
        }
    }

    // إعداد نموذج إرسال التقييم (Task 4)
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const placeId = getPlaceIdFromURL();
            const reviewText = document.getElementById('review-text').value;
            const rating = document.getElementById('rating').value;

            if (!placeId) {
                alert('Place ID is missing from URL.');
                return;
            }

            await submitReview(token, placeId, reviewText, rating);
        });
    }
});

// استخراج placeId من URL
function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id') || params.get('place_id');
}

// جلب الكوكي باسمها
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// التحقق من المصادقة والتوجيه
function checkAuthentication(redirectIfUnauth = false) {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const addReviewSection = document.getElementById('add-review');

    if (redirectIfUnauth && !token) {
        window.location.href = 'index.html';
        return null;
    }

    if (loginLink) {
        loginLink.style.display = token ? 'none' : 'inline-block';
    }

    if (addReviewSection) {
        addReviewSection.style.display = token ? 'block' : 'none';
    }

    if (document.getElementById('places-list')) {
        fetchPlaces(token);
    }

    return token;
}

// تسجيل الدخول
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

// جلب قائمة الأماكن
async function fetchPlaces(token) {
    try {
        const headers = { 'Content-Type': 'application/json' };
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const response = await fetch('/api/v1/places', { headers });
        if (response.ok) {
            const places = await response.json();
            displayPlaces(places);
        }
    } catch (error) {
        console.error('Error fetching places:', error);
    }
}

// عرض الأماكن
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

// جلب تفاصيل مكان
async function fetchPlaceDetails(token, placeId) {
    try {
        const headers = { 'Content-Type': 'application/json' };
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const response = await fetch(`/api/v1/places/${placeId}`, { headers });
        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place);
        }
    } catch (error) {
        console.error('Error fetching place details:', error);
    }
}

// عرض تفاصيل المكان
function displayPlaceDetails(place) {
    const placeDetails = document.getElementById('place-details');
    if (!placeDetails) return;

    placeDetails.innerHTML = '';

    const price = place.price_by_night || place.price || 0;
    const amenities = place.amenities || [];
    const reviews = place.reviews || [];

    const detailsHTML = `
        <h1>${place.title || place.name}</h1>
        <div class="place-info">
            <p><strong>Host:</strong> ${place.owner ? `${place.owner.first_name} ${place.owner.last_name}` : 'N/A'}</p>
            <p><strong>Price:</strong> $${price} per night</p>
            <p><strong>Description:</strong> ${place.description || 'No description provided.'}</p>
        </div>

        <div class="amenities">
            <h2>Amenities</h2>
            <ul>
                ${amenities.length > 0 
                    ? amenities.map(a => `<li>${a.name || a}</li>`).join('') 
                    : '<li>No amenities listed</li>'}
            </ul>
        </div>

        <div class="reviews">
            <h2>Reviews</h2>
            <div id="reviews-list">
                ${reviews.length > 0 
                    ? reviews.map(r => `
                        <div class="review-card">
                            <p><strong>${r.user_name || r.user ? `${r.user.first_name}` : 'Anonymous'}:</strong> ${r.text || r.comment}</p>
                            <p>Rating: ${r.rating || 5}/5</p>
                        </div>
                    `).join('') 
                    : '<p>No reviews yet.</p>'}
            </div>
        </div>
    `;

    placeDetails.innerHTML = detailsHTML;
}

// إرسال التقييم إلى API (Task 4)
async function submitReview(token, placeId, reviewText, rating) {
    try {
        const response = await fetch('/api/v1/reviews', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                place_id: placeId,
                text: reviewText,
                rating: parseInt(rating)
            })
        });

        if (response.ok) {
            alert('Review submitted successfully!');
            document.getElementById('review-form').reset();
            window.location.href = `place.html?id=${placeId}`;
        } else {
            const errorData = await response.json().catch(() => ({}));
            alert('Failed to submit review: ' + (errorData.message || response.statusText));
        }
    } catch (error) {
        console.error('Error submitting review:', error);
        alert('Could not submit review. Check network or backend server.');
    }
}
