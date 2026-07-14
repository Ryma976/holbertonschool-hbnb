# Part 2: HBnB Evolution - Core Business Logic Classes

## Project Overview
This part focuses on bringing the architectural design of the HBnB Evolution application to life by implementing the Business Logic Layer and Presentation Layer using Python, Flask, and Flask-RESTx.

## Task 1: Core Business Logic Classes
In this task, we implemented the fundamental core domain models following clean object-oriented programming (OOP) principles, data validations, and logical integrity rules.

### Implemented Models & Structural Hierarchy
1. **BaseModel (`app/models/base.py`):** The universal parent entity class that generates system attributes for audit trails, including a unique identifier (`id` via UUID4), alongside automated generation for creation (`created_at`) and modification (`updated_at`) timestamps.
2. **User (`app/models/user.py`):** Manages subscriber records. Validates first names, last names, and ensures strict global validation on email payload formatting patterns.
3. **Amenity (`app/models/amenity.py`):** Represents features or services offered by properties (e.g., Wi-Fi, Pool). Ensures required validation checks prevent empty descriptor profiles.
4. **Review (`app/models/review.py`):** Captures property feedback. Enforces explicit constraints keeping numeric user rating metrics strictly within the 1-to-5 star threshold.
5. **Place (`app/models/place.py`):** The primary transaction entity. It establishes compositional associations by mapping property metadata against latitude/longitude global constraints and enforcing strictly positive numeric limits for pricing models.

---

## Technical Directory Structure
```text
part2/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   └── amenity.py
│   ├── services/
│   │   └── facade.py
│   └── persistence/
│       └── repository.py
├── run.py
└── requirements.txt