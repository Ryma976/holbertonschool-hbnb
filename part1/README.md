HBnB Evolution - Part 1: Technical Documentation

Task 0: High-Level Package Diagram

📊 Interactive High-Level Package Diagram

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
----
# 1. Detailed Class Diagram for Business Logic Layer
```mermaid
classDiagram
    %% Core System Components & Interfaces
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

    %% Relationships and Design Patterns
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
# HBnB Evolution: Technical Documentation - Task 2 (Sequence Diagrams)
#2. Sequence Diagrams for API Calls
## 1. User Registration
This diagram captures the workflow when a user signs up for a new account.

```mermaid
sequenceDiagram
    autonumber
    actor Client as Client / User
    participant API as Presentation (UserAPI)
    participant Facade as BLL (HBnB Facade)
    participant Service as BLL (UserService)
    participant DB as Persistence (UserRepository)

    Client->>API: POST /api/v1/users (JSON payload)
    activate API
    API->>API: Validate Input (Check email & password format)
    
    API->>Facade: register_user(registration_data)
    activate Facade
    
    Facade->>Service: create_user(registration_data)
    activate Service
    
    Service->>DB: find_by_email(email)
    activate DB
    DB-->>Service: Return User Object / None
    deactivate DB
    
    alt Email already registered
        Service-->>Facade: Raise Exception (UserExistsError)
        Facade-->>API: Return Error Status Mapping
        API-->>Client: HTTP 400 Bad Request (Message: Email exists)
    else Email is unique
        Service->>Service: Hash password & instantiate User
        Service->>DB: save(user_instance)
        activate DB
        DB-->>Service: Confirm Persisted Entity
        deactivate DB
        
        Service-->>Facade: Return created User object
        deactivate Service
        
        Facade-->>API: Return User DTO Data
        deactivate Facade
        
        API-->>Client: HTTP 201 Created (JSON User Representation)
    end
    deactivate API


```
#2. Place Creation 
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
---
#3. Review Submission 
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
---
#4. Fetching a List of Places 
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

