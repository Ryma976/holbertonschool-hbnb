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
## 🛠️ Task 1: Core Business Logic Classes
We implemented the core domain models using Object-Oriented Programming (OOP) principles, ensuring correct relationships and strict attribute validation:

BaseModel (Base_Model.py): Universal parent entity class generating IDs via UUID4 and tracking creation (created_at) and modification (updated_at) timestamps.

User (user.py): Validates email format patterns, first name, and last name.

Amenity (amenity.py): Enforces non-empty descriptors (e.g., WiFi, Pool).

Place (place.py): Establishes compositional association with its owner and amenities, and enforces positive numeric limits for price, latitude, and longitude.

Review (review.py): Captures feedback. Enforces rating metrics strictly within a 1-to-5 star threshold and connects a user_id to a place_id
## 📬 API Endpoints (Tasks 2, 3, 4, & 5)
Our RESTful API is built using Flask-RESTx, which auto-generates interactive Swagger documentation.

1. Users Management (/api/v1/users/)
POST / - Register a new user with email validation.

GET / - Retrieve all registered users.

GET /<user_id> - Get detailed user information.

PUT /<user_id> - Update user details.

2. Amenities Management (/api/v1/amenities/)
POST / - Create a new amenity.

GET / - Retrieve all amenities.

GET /<amenity_id> - Get details of a specific amenity.

PUT /<amenity_id> - Update an amenity's name/description.

3. Places Management (/api/v1/places/)
POST / - Create a place (validates that owner_id exists and maps amenity_ids).

GET / - Retrieve all places.

GET /<place_id> - Get detailed place info (includes nested serialized objects of the owner, list of amenities, and associated reviews).

PUT /<place_id> - Update place details.

4. Reviews Management (/api/v1/reviews/ - Task 5)
POST / - Submit a review for a place (validates user_id, place_id, non-empty text, and a rating between 1 and 5).

GET / - List all reviews.

GET /<review_id> - Retrieve specific review details.

PUT /<review_id> - Update a review's rating or text.

DELETE /<review_id> - Deletes a review from the persistence layer (this is the only entity supporting deletion in this part).

### How to Run and Test the Application

### 1. Installation
Navigate to the part2 directory and install the necessary requirements:

```bash
cd part2
pip install -r requirements.txt
```
### 2. Run Server
Execute the application entry script:
```bash
python run.py
```
### 3. Interactive Testing (Swagger UI)
Open your web browser and navigate to:
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

You can use the interactive Swagger UI panel to perform, test, and document all CRUD requests on Users, Amenities, Places, and Reviews.
## 🧪 Testing and Validation (Task 6)
We have written comprehensive unit tests for both business logic (models) and API endpoints inside the tests/ directory.

Running Automated Unit Tests
To run the entire test suite and verify that all validations, API status codes, and edge cases are handled correctly:

```Bash
python -m unittest discover -s tests
```
## Manual Testing with cURL
You can also manually test endpoints. For example, creating a new review:
```Bash
curl -X POST "[http://127.0.0.1:5000/api/v1/reviews/](http://127.0.0.1:5000/api/v1/reviews/)" \
     -H "Content-Type: application/json" \
     -d '{"text": "Amazing place, highly recommended!", "rating": 5, "user_id": "<USER_ID>", "place_id": "<PLACE_ID>"}'
```


<img width="1582" height="896" alt="2" src="https://github.com/user-attachments/assets/cfe935f8-32ad-468e-b4bd-b62d41f4bea5" />
<img width="1695" height="903" alt="1" src="https://github.com/user-attachments/assets/425b0cc4-36a1-4a79-8758-5018f9c3a1c6" />


## Authors:
- Reem Alanazi
- Bayadir Aldossari
- Shomokh Aldossari
---


