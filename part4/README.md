# 🏰 HBnB — Front-End Web Client (Part 4)

Welcome to the front-end client interface for the **HBnB Application**. This dynamic web portal interacts asynchronously with the Flask RESTful API engine built in `part3`.

---

## 📁 Project Architecture

```text
part4/
├── images/             # UI icons, place placeholders, and media assets
├── index.html          # Main hub displaying available places & filters
├── login.html          # User authentication portal
├── register.html       # New user account registration form
├── place.html          # Extended place detail breakdown & review list
├── add_review.html     # Authenticated review submission page
├── styles.css          # Design system, layout rules, & UI component styles
├── scripts.js          # ES6 API integration, JWT handling, & DOM controllers
├── .gitignore          # Repository exclusion rules
└── README.md           # Project documentation

```

---

## 🚀 Pages & Core Functionality

* **`index.html`**: Catalog displaying available properties using dynamic `.place-card` modules with country/price filtering.
* **`login.html`**: Secure login interface interacting with the auth endpoint to set session JWT tokens in cookies.
* **`register.html`**: Onboarding form allowing new guests to join the platform.
* **`place.html`**: Displays individual property spec pages including host info, amenities, and dynamic `.review-card` elements.
* **`add_review.html`**: Protected review creation interface for verified logged-in users.

---

## 📐 Design System & UI Rules

All dynamic components adhere strictly to the layout parameters:

* **Margin**: `20px`
* **Padding**: `10px`
* **Border**: `1px solid #ddd`
* **Border Radius**: `10px`

### Mandatory CSS Selectors

`.logo` • `.login-button` • `.place-card` • `.details-button` • `.place-details` • `.place-info` • `.review-card` • `.form` • `.add-review`

---

## ⚙️ How to Run & Test

### 1. Launch Backend API (`part3`)

Start the Flask backend server:

```bash
cd ~/holbertonschool-hbnb/part3
python3 run.py

```

### 2. Launch Front-End Web Client (`part4`)

In a new terminal tab, spin up the HTTP web server:

```bash
cd ~/holbertonschool-hbnb/part4
python3 -m http.server 8000

```

> **Preview Access:** Open `[http://127.0.0.1:8000/login.html](http://127.0.0.1:8000/login.html)` in your web browser or use the platform's active **Port Preview (8000)**.

---

## 👥 Authors

* **Bayadir Aldossari**
* **Reem Alanazi**
* **Shomukh Aldosari**
