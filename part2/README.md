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

##Authors:
- Reem Alanazi
- Bayadir Aldossari
- Shomokh Aldossari
---
