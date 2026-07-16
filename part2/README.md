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
`````

### 2. The Facade Design Pattern
To prevent tight coupling between the Presentation Layer (API Endpoints) and the Business Logic Layer (Models/Repository), we integrated the Facade Pattern (HBnBFacade).

Instead of the API Endpoints calling the Repository or creating Models directly, all requests funnel through a single entry point:

Simplification: API endpoints don't need to know how the models establish relationships (e.g., how a Place links to an owner_id or registers amenity_ids).

Decoupling: If we later change how data is validated, stored, or managed under the hood, we only modify the Facade class without breaking any API endpoint codes.

### 3. Understanding In-Memory Persistence in HBnB
Since SQL-backed databases will be integrated later in Part 3, we use a fully functional InMemoryRepository class to handle storage operations temporarily during application runtime.

It utilizes standard Python dictionaries to store data objects as key-value pairs indexed by unique IDs (UUID).

It abstracts storage functions (add, get, get_all, update, delete) using abstract methods so that when we swap to SQL-Alchemy in Part 3, the codebase switch will be seamless.

## Technical Directory Structure
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
├── README.md
`````
### How to Run and Test the Application
1. Installation
Navigate to the part2 directory and install the necessary requirements:
cd part2
pip install -r requirements.txt

### 2. Run Server
Execute the application entry script:
python run.py

### 3. Interactive Testing (Swagger UI)
Open your web browser and navigate to:
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

You can use the interactive Swagger UI panel to perform, test, and document all CRUD requests on Users, Amenities, Places, and Reviews.

## Authors:
- Reem Alanazi
- Bayadir Aldossari
- Shomokh Aldossari
---
