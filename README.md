# Part 1: Technical Documentation - HBnB Evolution

## 1. Introduction
This comprehensive technical documentation serves as the architecture blueprint and detailed system design for the **HBnB Evolution** application. HBnB Evolution is a simplified, customized property rental platform designed to manage users, property listings (places), customer feedback (reviews), and feature specifications (amenities). 

The purpose of this document is to establish a rigorous structural foundation, explicit entity relationships, and clear transactional lifecycles across the system’s layers. By outlining the high-level architecture and dynamic behavioral patterns using standard UML notations, this blueprint ensures a predictable, secure, and maintainable implementation phase in the subsequent parts of the project.

---

## 2. High-Level Architecture
The HBnB Evolution application enforces a strict separation of concerns by leveraging a traditional **3-Tier Layered Architecture Pattern**, augmented by the **Facade Design Pattern**. This structural boundary isolates individual systemic responsibilities and protects the database state from direct client interaction.

### High-Level Package Diagram

```mermaid
packageDiagram
    package "Presentation Layer" as Presentation {
        [API Controllers]
        [Data Transfer Objects (DTOs)]
    }

    package "Business Logic Layer" as BusinessLogic {
        [HBnB API Facade] as Facade
        
        package "Core Entities" as Entities {
            [User]
            [Place]
            [Review]
            [Amenity]
        }
        
        package "Services" as Services {
            [UserService]
            [PlaceService]
            [ReviewService]
            [AmenityService]
        }
    }

    package "Persistence Layer" as Persistence {
        [Repository Interfaces]
        [Database Repositories]
    }

    %% System Dependencies and Data Flows
    [API Controllers] --> Facade : Dispatches Requests
    Facade --> Services : Coordinates Operations
    Services --> Entities : Manipulates State
    Services --> [Repository Interfaces] : Persists/Retrieves Data
    [Database Repositories] --|> [Repository Interfaces] : Implements

```

---
#Detailed Class Diagram
Architectural Explanatory Notes
#Presentation Layer: Actively consumes incoming RESTful HTTP requests via specialized API Controllers. It abstracts network payload parameters using Data Transfer Objects (DTOs) to perform early-stage syntactic validation before forwarding data downstream.

#Business Logic Layer (BLL): Contains the core application models, structural domain entities, and operational validation workflows. To maintain a clean interface between the outer presentation components and inner subsystems, the HBnB API Facade acts as a centralized mediator. Presentation controllers call only the Facade, which orchestrates communication among specialized internal services (UserService, PlaceService, etc.).

#Persistence Layer: Abstract repository interfaces isolate core application services from the mechanics of concrete database storage engines. This allows data layer implementations to be swapped transparently without disrupting domain logic.

#3. Business Logic Layer Model
#The domain structure follows clean object-classDiagram
    class BaseModel {
        +UUID id
        +DateTime created_at
        +DateTime updated_at
        +save() void
        +update(dict attributes) void
    }

    class User {
        +String first_name
        +String last_name
        +String email
        +String password
        +Boolean is_admin
        +register() Boolean
        +update_profile(dict profile_data) void
    }

    class Place {
        +String title
        +String description
        +Float price
        +Float latitude
        +Float longitude
        +UUID owner_id
        +create_place() Place
        +add_amenity(Amenity amenity) void
        +get_reviews() List~Review~
    }

    class Review {
        +Integer rating
        +String comment
        +UUID place_id
        +UUID user_id
        +post_review() Review
    }

    class Amenity {
        +String name
        +String description
        +create_amenity() Amenity
    }

    %% Inheritance Connections
    BaseModel <|-- User
    BaseModel <|-- Place
    BaseModel <|-- Review
    BaseModel <|-- Amenity

    %% Association Connections
    User "1" --> "0..*" Place : owns
    User "1" --> "0..*" Review : writes
    Place "1" *-- "0..*" Review : contains
    Place "0..*" o-- "0..*" Amenity : has (Many-to-Many)oriented principles. To ensure auditability and consistent system tracking, all specific entity entities inherit system traits from a unified base class.
---

