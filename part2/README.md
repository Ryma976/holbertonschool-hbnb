# HBnB Evolution - Part 2: Project Setup & Package Initialization

Welcome to the implementation phase of the **HBnB Evolution** project. This documentation covers the foundation of our modular architecture (Task 0), designed to establish a clean separation of concerns using a three-layer architecture pattern combined with the Facade design pattern and an In-Memory Persistence system.

---

## 🏛️ Conceptual Architecture & Design Patterns

To understand the core design decisions implemented in this phase, we look closely at three main concepts:

### 1. Three-Layer Architecture
The application codebase is strictly organized into three independent layers to ensure high maintainability, modularity, and clean boundaries:

```text
+-------------------------------------------------------------+
|                     PRESENTATION LAYER                      |
|            (Flask Endpoints & Swagger /api/v1/)             |
+-------------------------------------------------------------+
                              |
                              v [Request / Payload Data]
+-------------------------------------------------------------+
|                    BUSINESS LOGIC LAYER                     |
|           (Models: User, Place, Amenity, Review)            |
+-------------------------------------------------------------+
                              |
                              v [Persistent Models]
+-------------------------------------------------------------+
|                      PERSISTENCE LAYER                      |
|                (InMemoryRepository Storage)                 |
+-------------------------------------------------------------+
---
`````

##Technical Directory Structure
The project directory structure is set up cleanly according to standard Python packaging best practices:
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
├── README.mdx
`````


##Authors:
- Reem Alanazi
- Bayadir Aldossari
- Shomokh Aldossari
---
