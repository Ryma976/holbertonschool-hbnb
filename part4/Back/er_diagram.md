# HBnB Database ER Diagram

Below is the Entity-Relationship Diagram representing the database schema for the HBnB project.

```mermaid
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
