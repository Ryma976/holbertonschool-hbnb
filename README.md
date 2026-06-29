# HBnB Evolution - Part 1: Technical Documentation

## Task 0: High-Level Package Diagram

### 📊 Interactive UML Diagram
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
```

    API_Endpoints --> HBnB_Facade : Uses Facade
    HBnB_Facade --> Core_Models : Manages
    Core_Models --> Repository : Persists Data

---

## Task 1: Detailed Class Diagram for Business Logic Layer

### 📊 Interactive UML Class Diagram









