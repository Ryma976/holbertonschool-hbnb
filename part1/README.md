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
### Description

Illustrates the 3-tier architecture (Presentation, Business Logic, Persistence) and uses the **Facade Pattern** to decouple layers.

* **Presentation Layer**: Handles API endpoints, user interface interactions.
* **Business Logic Layer**: Contains core operations and validation logic.
* **Persistence Layer**: Manages database interactions.
  
### Explanation:
- The **User**, **Place**, **Review**, and **Amenity** entities represent the main components of the system.
- The **Presentation Layer** (UI and API) interacts directly with the business models in the Business Logic Layer.
- Each business entity interacts with its corresponding repository in the Persistence Layer to store and retrieve data.

The system design employs the **Facade Pattern** between the Presentation Layer and Business Logic Layer to simplify interaction and isolate complexity. Below is the high-level architecture diagram:


---

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

This diagram represents the entities of this layer, their attributes, methods, and relationships. The main objective is to provide a clear and detailed visual representation of the core business logic, focusing on the key entities: 
- User
- Place
- Review
- Amenity
### Explanation:


Each core business entity is modeled with a base class that includes basic functionalities like creating, updating, and deleting entries:

- The **Entity** base class provides common functionalities such as create, update, and delete for all business entities.
- The **User** class manages user-related information and operations such as registering and updating user details.
- The **Place** class represents accommodation listings, storing details like price and location.
- the **Review** classe associated with a user place contains comments that user can give to a place.
- the **Amenity** classe associated to user's place contains all the commodities belongin to a user's place

The diagram details the attributes and methods, the relationships between classes (`1-to-N`, `N-to-N`), the timestamps (`created_at`, `updated_at`), and the unique identifiers (IDs).
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

Sequence diagrams help visualize how different system components interact to address specific use cases, illustrating the step-by-step process of handling API requests. There will be four of them flow : 
- User Registration
- Place Creation
- Review Submission
- Place Listing
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
## Design Considerations

- Clear separation between layers
- Business Logic is isolated from direct database access
- API acts as the system entry point
- UML standards followed for clarity and consistency

---

### Conclusion

These diagrams provide a clear overview of:
- System **structure** (Class & Package diagrams)
- System **behavior** (Sequence diagrams)

They collectively explain how the HBnB application is designed and how data flows across its layers.
---
##     Resources

### UML Basics
- *OOP – Introduction to UML*

### Package Diagrams
- *UML Package Diagram Overview*  
- *UML Package Diagrams Guide*

### Class Diagrams
- *UML Class Diagram Tutorial*  
- *How to Draw UML Class Diagrams*

### Sequence Diagrams
- *UML Sequence Diagram Tutorial*  
- *Understanding Sequence Diagrams*

### Diagram Tools
- Mermaid.js  
- draw.io  

---
## Authors:
- Reem Alanazi
- Bayadir Aldossari
- Shomokh Aldossari

---
