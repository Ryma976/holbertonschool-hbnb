# HBnB Part 4 — Front-End Web Client

## Overview

This directory contains the front-end application for HBnB, constructed using **HTML5**, **CSS3**, and **JavaScript (ES6)**. It connects asynchronously with the Flask RESTful API located in the `part4/Back` directory.

---

## Folder Structure

```text
part4/Front/
├── images/             # Icons and place card image assets
├── index.html          # Main page displaying all places
├── login.html          # User authentication form
├── register.html       # New user registration form
├── place.html          # Detailed place view and review list
├── add_review.html     # Authenticated review submission form
├── styles.css          # Main stylesheet
├── scripts.js         # JavaScript ES6 API integration & session logic
├── .gitignore          # Git exclusion rules
└── README.md           # Documentation file

```
## Page Routes & Functionalities

- **`index.html`**: Displays a catalog of available places using card components (`.place-card`) and dynamic country filtering.
- **`login.html`**: Form for authenticating users via API and storing session JWT tokens in cookies.
- **`register.html`**: Form allowing new users to create accounts.
- **`place.html`**: Shows extended details for a specific place including host, price, amenities, and user reviews (`.review-card`).
- **`add_review.html`**: Accessible to logged-in users for submitting new place reviews.

---

## Design Specifications

All place and review card components adhere strictly to required UI parameters:

- **Margin**: `20px`
- **Padding**: `10px`
- **Border**: `1px solid #ddd`
- **Border Radius**: `10px`

### Mandatory Classes
`.logo`, `.login-button`, `.place-card`, `.details-button`, `.place-details`, `.place-info`, `.review-card`, `.form`, `.add-review`
---
## How to Run Locally

Start a simple web server within the `Front` directory:

```bash
cd part4/Front
python3 -m http.server 8000
```
### 🧑‍💻 Authors
Bayadir Aldossari

Reem Alanazi

Shomokh Aldosari
