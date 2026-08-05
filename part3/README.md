cd ~/holbertonschool-hbnb/part3

cat << 'EOF' > README.md
# HBnB - Part 3: Database Integration and Persistence

## 📝 Overview
This part of the HBnB project shifts the application architecture from in-memory data storage to a persistent relational database using **SQLAlchemy ORM** and **SQLite/MySQL**. It establishes full entity mapping, authentication database persistence, database initialization scripts, and visual ER diagramming.

---

## 🚀 Tasks Breakdown

### Task 0: Database Selection & Environment Setup
- Configured the development environment to support relational databases using **SQLAlchemy** and **Flask-SQLAlchemy**.
- Prepared environment configurations for switching between repository types (in-memory vs. database).

### Task 1: Base Model & SQLAlchemy Integration
- Updated `BaseModel` to inherit from `db.Model`.
- Added standard database columns: `id` (UUID Primary Key), `created_at`, and `updated_at`.
- Implemented core persistence methods: `save()`, `delete()`, and `to_dict()`.

### Task 2: User Entity Mapping
- Mapped the `User` class to the `users` table using SQLAlchemy columns.
- Implemented unique constraints for `email` and secure password hashing integration with `flask_bcrypt`.

### Task 3: Place, Review, and Amenity Entities Mapping
- Mapped remaining core models to their database tables:
  - `Place` -> `places`
  - `Review` -> `reviews`
  - `Amenity` -> `amenities`
- Enforced validation rules, default column parameters, and non-nullable fields.

### Task 4 & 5: Authentication Persistence & JWT Integration
- Updated authentication logic to query users from the persistent database instead of memory.
- Ensured JWT token generation and authorization mechanisms function seamlessly with database entities.

### Task 6 & 7: Database Repository Pattern Implementation
- Created `SQLAlchemyRepository` implementing the generic repository interface.
- Enabled standard CRUD database operations (`add`, `get`, `get_all`, `update`, `delete`).

### Task 8: Entity Relationships Mapping
- Mapped relational connections across models using SQLAlchemy `db.relationship` and `db.ForeignKey`:
  - **One-to-Many**: `User` ➔ `Place` (Owner)
  - **One-to-Many**: `User` ➔ `Review` (Author)
  - **One-to-Many**: `Place` ➔ `Review`
  - **Many-to-Many**: `Place` ↔ `Amenity` (via `place_amenity` junction table).

### Task 9: SQL Scripts for Schema & Initial Data
- Created raw SQL automation scripts:
  - `schema.sql`: Full DDL script to create tables, constraints, primary keys, and foreign keys with cascading deletions.
  - `seed.sql`: Initial dataset insertion script adding an administrator account (`admin@hbnb.io`) and default amenities.

### Task 10: ER Diagram Generation
- Designed a comprehensive Entity-Relationship Diagram using **Mermaid.js** syntax in `er_diagram.md` to visually document table architectures and cardinality.

---

## 📐 ER Diagram Overview

```mermaid
erDiagram
    USERS ||--o{ PLACES : "owns"
    USERS ||--o{ REVIEWS : "writes"
    PLACES ||--o{ REVIEWS : "has"
    PLACES ||--|{ PLACE_AMENITY : "contains"
    AMENITIES ||--|{ PLACE_AMENITY : "belongs_to"
