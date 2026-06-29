graph TB
    %% Presentation Layer
    subgraph Presentation_Layer [Presentation Layer]
        A[API Endpoints / Routers] --> B[Services / Controllers]
    end

    %% Business Logic Layer
    subgraph Business_Logic_Layer [Business Logic Layer]
        direction TB
        Facade[HBnB Facade Interface]
        
        subgraph Models [Core Models]
            M1[User]
            M2[Place]
            M3[Review]
            M4[Amenity]
        end
        
        Facade --> Models
    end

    %% Persistence Layer
    subgraph Persistence_Layer [Persistence Layer]
        Repository[Data Repositories / DAOs] --> DB[(Database / Storage)]
    end

    %% Communication Pathways via Facade
    Presentation_Layer -->|Calls Unified Interface| Facade
    Business_Logic_Layer -->|Data Retrieval / Persistence| Persistence_Layer

    %% Styling
    style Presentation_Layer fill:#f9f0ff,stroke:#d3adf7,stroke-width:2px
    style Business_Logic_Layer fill:#e6f7ff,stroke:#91d5ff,stroke-width:2px
    style Persistence_Layer fill:#f6ffed,stroke:#b7eb8f,stroke-width:2px
    style Facade fill:#fffbe6,stroke:#ffe58f,stroke-width:2px,font-weight:bold
