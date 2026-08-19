document.addEventListener('DOMContentLoaded', () => {
    // 1. التعامل مع نموذج تسجيل الدخول (Task 1)
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            await loginUser(email, password);
        });
    }

    // 2. جلب الأماكن وتصفيتها (Task 2)
    const placesList = document.getElementById('places-list');
    const countryFilter = document.getElementById('country-filter');

    if (placesList) {
        fetchPlaces(); // جلب الأماكن عند فتح الصفحة

        if (countryFilter) {
            countryFilter.addEventListener('change', (event) => {
                const selectedCountry = event.target.value;
                filterPlaces(selectedCountry);
            });
        }
    }
});

// دالة تسجيل الدخول
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
            // حفظ التوكين في الـ Cookie
            document.cookie = `token=${data.access_token}; path=/; max-age=86400`;
            // التوجيه للصفحة الرئيسية
            window.location.href = 'index.html';
        } else {
            const errorData = await response.json().catch(() => ({}));
            alert('فشل تسجيل الدخول: ' + (errorData.message || 'بيانات غير صحيحة'));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('تعذر الاتصال بالسيرفر. تأكدي أن سيرفر الباك إند شغّال.');
    }
}

// دالة جلب الأماكن من الباك إند
let allPlaces = [];

async function fetchPlaces() {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/places');
        if (response.ok) {
            allPlaces = await response.json();
            displayPlaces(allPlaces);
        } else {
            console.error('Failed to fetch places');
        }
    } catch (error) {
        console.error('Error fetching places:', error);
    }
}

// دالة عرض الأماكن في الصفحة
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    placesList.innerHTML = '';

    places.forEach(place => {
        const placeCard = document.createElement('div');
        placeCard.className = 'place-card';
        placeCard.setAttribute('data-country', place.country || '');

        placeCard.innerHTML = `
            <h2>${place.title}</h2>
            <p>Price per night: $${place.price_by_night}</p>
            <p>Location: ${place.city_name || ''}, ${place.country_name || ''}</p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;
        placesList.appendChild(placeCard);
    });
}

// دالة تصفية الأماكن حسب الدولة
function filterPlaces(country) {
    if (country === 'All' || country === '') {
        displayPlaces(allPlaces);
    } else {
        const filtered = allPlaces.filter(place => place.country === country || place.country_name === country);
        displayPlaces(filtered);
    }
}
