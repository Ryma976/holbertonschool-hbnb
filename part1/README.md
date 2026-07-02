#
# HBnB Evolution - Part 1: Technical Documentation

This document presents the technical design of the HBnB Evolution application (Part 1). It provides the UML diagrams that describe the system architecture, the main business entities, and the interactions between application layers.

The documentation includes:

- High-Level Package Diagram
- Business Logic Class Diagram
- Sequence Diagrams

---

## Task 0: High-Level Package Diagram

This diagram presents the overall architecture of the application using a three-layer design. It also illustrates how the Presentation Layer communicates with the Business Logic Layer through the Facade pattern, while the Business Logic Layer interacts with the Persistence Layer for data storage.
. Package Diagram

```mermaid
classDiagram
    namespace Presentation_Layer {
        class API_Endpoints {
            +UserRoutes
            +PlaceRoutes
            +ReviewRoutes
            +AmenityRoutes
        }
    }

    namespace Business_Logic_Layer {
        class HBnB_Facade {
            <<Interface>>
            +register_user()
            +create_place()
            +add_review()
        }

        class Core_Models {
            +User
            +Place
            +Review
            +Amenity
        }
    }

    namespace Persistence_Layer {
        class Repository {
            +InMemoryRepository
            +DatabaseRepository
        }
    }

    API_Endpoints --> HBnB_Facade : Uses Facade
    HBnB_Facade --> Core_Models : Manages
    Core_Models --> Repository : Persists Data
```

---

## Task 1: Detailed Class Diagram for Business Logic Layer

The following class diagram represents the main business entities of the system. It includes their attributes, operations, inheritance relationships, and associations that define how the entities interact with one another.

```mermaid
classDiagram
    class BaseEntity {
        <<Abstract>>
        +UUID4 id
        +datetime created_at
        +datetime updated_at
        +save() void
        +update(dict kwargs) void
    }

    class User {
        +string first_name
        +string last_name
        +string email
        +string password
        +bool is_admin
        +register() bool
        +update_profile(dict data) bool
    }

    class Place {
        +string title
        +string description
        +float price
        +float latitude
        +float longitude
        +UUID4 owner_id
        +create_place() bool
        +update_details(dict data) bool
        +add_amenity(UUID4 amenity_id) void
    }

    class Review {
        +string text
        +int rating
        +UUID4 place_id
        +UUID4 user_id
        +submit_review() bool
    }

    class Amenity {
        +string name
        +string description
        +create_amenity() bool
    }

    BaseEntity <|-- User : Generalization (Inheritance)
    BaseEntity <|-- Place : Generalization (Inheritance)
    BaseEntity <|-- Review : Generalization (Inheritance)
    BaseEntity <|-- Amenity : Generalization (Inheritance)

    User "1" --> "0..*" Place : Owns / Hosts
    User "1" --> "0..*" Review : Writes
    Place "1" *-- "0..*" Review : Contains (Composition)
    Place "0..*" --> "0..*" Amenity : Associated With (Aggregation)
```

---

## Task 2: Sequence Diagrams for API Calls

The following sequence diagrams describe how requests move through the Presentation, Business Logic, and Persistence layers for common application operations.

### 1. User Registration

This sequence shows the process of creating a new user account, including input validation, uniqueness verification, data persistence, and the response returned to the client.

```mermaid
sequenceDiagram
    autonumber
    actor Client as Client / User
    participant API as Presentation (UserAPI)
    participant Facade as BLL (HBnB Facade)
    participant Model as BLL (User Model)
    participant DB as Persistence (UserRepository)

    Client->>API: POST /api/v1/users (JSON payload)
    API->>API: Validate Input Format (Email & Password)
    API->>Facade: register_user(registration_data)
    Facade->>Model: Validate Constraints (Email Unique)
    Model->>DB: find_by_email(email)
    DB-->>Model: Return User Object / None

    alt Email already exists
        Model-->>Facade: Raise Exception (UserExistsError)
        Facade-->>API: Return Error Status Mapping
        API-->>Client: HTTP 400 Bad Request (Email exists)
    else Email is unique
        Model->>Model: Hash Password & Generate UUID
        Model->>DB: save(user_instance)
        DB-->>Model: Confirm Persisted Entity
        Model-->>Facade: Return created User object
        Facade-->>API: Return User DTO Data
        API-->>Client: HTTP 201 Created (JSON Representation)
    end
```

### 2. Place Creation

This sequence illustrates how a new place is created, validated, stored, and returned to the client after successful processing.

```mermaid
sequenceDiagram
    autonumber
    actor Client as Owner (User)
    participant API as Presentation (PlaceAPI)
    participant Facade as BLL (HBnB Facade)
    participant Model as BLL (Place Model)
    participant DB as Persistence (PlaceRepository)

    Client->>API: POST /api/v1/places (JSON payload)
    API->>API: Validate Base Required Fields
    API->>Facade: create_place(place_data)
    Facade->>Model: Initialize Place (Link to owner_id)
    Model->>Model: Validate Price (> 0) & Coordinates
    Model->>DB: save(place_instance)
    DB-->>Model: Confirm Save Operation
    Model-->>Facade: Return Place Entity
    Facade-->>API: Return Place DTO Data
    API-->>Client: HTTP 201 Created (JSON Place Object)
```

### 3. Review Submission

This sequence demonstrates how a review is validated, saved, and returned after a successful submission.

```mermaid
sequenceDiagram
    autonumber
    actor Client as Reviewer (User)
    participant API as Presentation (ReviewAPI)
    participant Facade as BLL (HBnB Facade)
    participant Model as BLL (Review Model)
    participant DB as Persistence (ReviewRepository)

    Client->>API: POST /api/v1/reviews (JSON payload)
    API->>Facade: add_review(review_data)
    Facade->>Model: Instantiate Review (user_id & place_id)
    Model->>Model: Validate Rating Range (e.g., 1-5)
    Model->>DB: save(review_instance)
    DB-->>Model: Confirm Save Operation
    Model-->>Facade: Review Processed Successfully
    Facade-->>API: Return Review DTO Data
    API-->>Client: HTTP 201 Created (JSON Review Object)
```

### 4. Fetching a List of Places

This sequence describes how the application retrieves a filtered list of places and returns the formatted results to the client.

```mermaid
sequenceDiagram
    autonumber
    actor Client as User / Client
    participant API as Presentation (PlaceAPI)
    participant Facade as BLL (HBnB Facade)
    participant DB as Persistence (PlaceRepository)

    Client->>API: GET /api/v1/places (Optional Filters)
    API->>Facade: get_places(filters)
    Facade->>DB: fetch_all_matching(filters)
    DB-->>Facade: Return List of Place Entities
    Facade->>Facade: Convert Entities to DTOs / JSON Format
    Facade-->>API: Return Formatted Data List
    API-->>Client: HTTP 200 OK (Array of Places)
```
---
### Conclusion

These diagrams provide a clear overview of:
- System **structure** (Class & Package diagrams)
- System **behavior** (Sequence diagrams)

They collectively explain how the HBnB application is designed and how data flows across its layers.
---

## Authors:
- Reem Alanazi
- Bayadir Aldossari
- Shomokh Aldossari

---
