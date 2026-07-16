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
hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       ├── amenities.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── Base_Model.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── facade.py
│   ├── persistence/
│       ├── __init__.py
│       ├── repository.py
├── tests/
│   ├── test_amenity.py
│   ├── test_BaseModel.py
│   ├── test_facade.py
│   ├── test_place.py
│   ├── test_review.py
│   ├── test_user.py
│   ├── TestAmenitiesAPI.py
│   ├── TestPlacesAPI.py
│   ├── TestReviewsAPI.py
│   ├── TestUsersAPI.py
├── run.py
├── config.py
├── requirements.txt
├── README.md
