# 0. High-Level Package Diagram

## 1. Architectural Overview & Objective
The primary objective of this task is to establish a solid structural blueprint for the HBnB application through a **Three-Tier Layered Architecture**. By decoupling responsibilities across specialized layers and introducing the **Facade Design Pattern**, we ensure that the application remains scalable, easily testable, and maintainable.

---

## 2. Package Diagram (Mermaid.js Core)
*Note: GitHub natively renders the Mermaid block below into an interactive, high-quality visual diagram within your repository documentation.*

```mermaid
graph TB
    %% Presentation Layer Package Boundary
    subgraph Presentation_Layer ["Package: Presentation Layer (UI & API Ecosystem)"]
        direction LR
        API[API Endpoints / Routers] --> Services[Request Controllers]
    end

    %% Business Logic Layer Package Boundary
    subgraph Business_Logic_Layer ["Package: Business Logic Layer (Core Domain Object)"]
        direction TB
        Facade[HBnB Unified Application Facade]
        
        subgraph Domain_Models ["Sub-Package: Core Enterprise Models"]
            M1[User Model]
            M2[Place Model]
            M3[Review Model]
            M4[Amenity Model]
        end
        
        Facade --> Domain_Models
    end

    %% Persistence Layer Package Boundary
    subgraph Persistence_Layer ["Package: Persistence Layer (Data Durability System)"]
        direction LR
        Repo[Data Repositories / DAOs] --> DB[(Database / In-Memory Storage)]
    end

    %% Communication Flow Pipelines via Facade Pattern
    Services -->|1. Invokes Unified Method Interface| Facade
    Domain_Models -->|2. Offloads Object States / Fetches| Repo

    %% Formatting Elements for High-Contrast Visual Delivery
    style Presentation_Layer fill:#f9f0ff,stroke:#d3adf7,stroke-width:2px
    style Business_Logic_Layer fill:#e6f7ff,stroke:#91d5ff,stroke-width:2px
    style Persistence_Layer fill:#f6ffed,stroke:#b7eb8f,stroke-width:2px
    style Facade fill:#fffbe6,stroke:#ffe58f,stroke-width:2px,font-weight:bold
