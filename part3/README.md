# HBnB Part 3 — Authentication and Database Persistence

## Description

Part 3 extends the HBnB backend with authentication, authorization, password hashing, and relational database persistence using **SQLAlchemy** and a **SQLite** database.

The application manages four core entities:
- **Users**
- **Places**
- **Reviews**
- **Amenities**

This version replaces the in-memory repository layer from Part 2 with SQLAlchemy ORM models, persistent database tables, relational foreign keys, JWT authentication, and SQL setup scripts.

---

## Technology Stack

- **Python 3**
- **Flask** & **Flask-RESTx**
- **Flask-SQLAlchemy** & **SQLAlchemy ORM**
- **Flask-Bcrypt** (Password Hashing)
- **Flask-JWT-Extended** (Authentication & Authorization)
- **SQLite3** (Database Engine)
- **Mermaid.js** (ER Diagramming)

---

## Project Structure

```text
part3/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── amenities.py
│   │       ├── auth.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       └── users.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── amenity.py
│   │   ├── base.py
│   │   ├── place.py
│   │   ├── review.py
│   │   └── user.py
│   ├── persistence/
│   │   ├── __init__.py
│   │   └── repository.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── facade.py
│   ├── __init__.py
│   └── extensions.py
├── er_diagram.md
├── hbnb_er_diagram.md
├── schema.sql
├── seed.sql
├── config.py
├── run.py
└── README.md
```
Architecture & Data Flow
Part 3 implements a layered architecture to decouple API routing, business logic, and database persistence:
API Layer (Flask-RESTx)
        │
        ▼
Facade Layer (Business Logic & Orchestration)
        │
        ▼
Repository Layer (SQLAlchemy ORM Data Access)
        │
        ▼
SQLite Database (development.db)
---
Database Schema & ER Diagram
The relational database architecture models connections between users, places, reviews, and amenities.

erDiagram
    USERS {
        VARCHAR_36 id PK
        VARCHAR_50 first_name
        VARCHAR_50 last_name
        VARCHAR_120 email UK
        VARCHAR_128 password
        BOOLEAN is_admin
        DATETIME created_at
        DATETIME updated_at
    }

    PLACES {
        VARCHAR_36 id PK
        VARCHAR_100 title
        TEXT description
        FLOAT price
        FLOAT latitude
        FLOAT longitude
        VARCHAR_36 owner_id FK
        DATETIME created_at
        DATETIME updated_at
    }

    REVIEWS {
        VARCHAR_36 id PK
        TEXT text
        INTEGER rating
        VARCHAR_36 place_id FK
        VARCHAR_36 user_id FK
        DATETIME created_at
        DATETIME updated_at
    }

    AMENITIES {
        VARCHAR_36 id PK
        VARCHAR_50 name
        DATETIME created_at
        DATETIME updated_at
    }

    PLACE_AMENITY {
        VARCHAR_36 place_id PK, FK
        VARCHAR_36 amenity_id PK, FK
    }

    USERS ||--o{ PLACES : "owns"
    USERS ||--o{ REVIEWS : "writes"
    PLACES ||--o{ REVIEWS : "has"
    PLACES ||--|{ PLACE_AMENITY : "contains"
    AMENITIES ||--|{ PLACE_AMENITY : "belongs_to"
    
