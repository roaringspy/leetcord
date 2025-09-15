# LeetCord: System Architecture

[cite_start]This document provides an exhaustive technical study and procedural guide for the development of a full-stack application centered around a social LeetCode browser extension. [cite: 3] [cite_start]The architecture is designed for robustness, scalability, and security, treating the project as a distributed system of microservices. [cite: 4]

## I. Architectural Blueprint: A Microservices Vision

[cite_start]This section establishes the high-level architecture, defines the flow of data and logic, and presents a curated technology stack. [cite: 5]

### 1.1. System Overview: Deconstructing the Application

[cite_start]The project is a system composed of four decoupled, yet interconnected, core services, alongside a dedicated data persistence layer. [cite: 8]

-   [cite_start]**The Browser Extension (Client/Frontend)**: The user-facing component built with JavaScript, HTML, and CSS. [cite: 10] [cite_start]Its primary responsibility is to detect a successful LeetCode submission and make a single, authenticated API call to the Backend API service with the problem's identifier. [cite: 11]
-   [cite_start]**The FastAPI API Server (Backend/Business Logic Layer)**: The central nervous system of the application, developed in Python using FastAPI. [cite: 13] [cite_start]It is responsible for all primary business logic, data processing, user authentication, score calculation, and dispatching events to the Discord Bot Service. [cite: 16, 13]
-   [cite_start]**The Discord Bot Service (Notification Layer)**: A standalone microservice managing interactions with Discord. [cite: 17] [cite_start]It runs a `discord.py` bot for handling commands and a concurrent FastAPI server to expose a secure internal API that listens for events from the Backend API Server. [cite: 18, 19, 20]
-   [cite_start]**The Scheduler (Automation Layer)**: A background job runner, implemented as a cron job, responsible for time-based automation like ending contests or triggering data cleanup. [cite: 21, 23]
-   [cite_start]**The Data Persistence Layer (Database/Storage Layer)**: The system's long-term memory, using **MongoDB Atlas**. [cite: 24] [cite_start]It communicates exclusively with the Backend API Server. [cite: 26]

### 1.2. Data and Logic Flow: From 'Submission' to 'Notification'

The primary user journey of a successful problem submission flows as follows:

1.  [cite_start]**Event Trigger**: A user successfully submits a solution on leetcode.com. [cite: 32]
2.  [cite_start]**Detection**: The browser extension's content script detects this success event. [cite: 33]
3.  [cite_start]**Secure API Call**: The extension's background service worker initiates a secure API call to the Python Backend API (e.g., `POST /api/v1/submissions`). [cite: 34]
4.  **Backend Verification and Processing**:
    -   [cite_start]The Backend API receives the request and validates the user's identity. [cite: 36]
    -   It checks its MongoDB database for cached problem info. [cite_start]If missing or stale, it fetches data from LeetCode's GraphQL API. [cite: 37, 38]
    -   [cite_start]The backend calculates the score, writes the new submission to MongoDB, and updates the user's contest score. [cite: 39, 40, 41]
5.  [cite_start]**Asynchronous Event Dispatch**: The Backend API sends a "fire-and-forget" event payload to the Discord Bot Service. [cite: 42, 43]
6.  [cite_start]**Real-time Notification**: The Discord Bot Service receives the event, formats a rich message, and sends it to the configured Discord channel. [cite: 44]

### 1.3. Technology Stack Recommendation

| Component | Technology | Rationale |
|---|---|---|
| **Backend API** | FastAPI (Python) | [cite_start]High-performance, async support, automatic data validation and documentation. [cite: 54] |
| **Discord Bot** | `discord.py` + FastAPI | [cite_start]Hybrid service combining real-time bot interactions with an internal API for receiving events. [cite: 55] |
| **Scheduler** | Cron | [cite_start]Robust, simple, and reliable for triggering API endpoints at fixed intervals. [cite: 58, 56] |
| **Database** | MongoDB Atlas | [cite_start]Fully managed, scalable NoSQL document database with a flexible schema. [cite: 59] |
| **Frontend UI** | Svelte | [cite_start]Modern UI compiler that produces highly optimized, minimal JavaScript for a fast user experience. [cite: 60] |
| **Deployment** | Docker, Google Cloud Run | [cite_start]Containerization for consistency, with serverless for the API and a container service for the long-running bot. [cite: 61] |