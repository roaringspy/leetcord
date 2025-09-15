# LeetCord: System Architecture

This document provides an exhaustive technical study and procedural guide for the development of a full-stack application centered around a social LeetCode browser extension. The architecture is designed for robustness, scalability, and security, treating the project as a distributed system of microservices.

## I. Architectural Blueprint: A Microservices Vision

This section establishes the high-level architecture, defines the flow of data and logic, and presents a curated technology stack.

### 1.1. System Overview: Deconstructing the Application

The project is a system composed of four decoupled, yet interconnected, core services, alongside a dedicated data persistence layer.

* **The Browser Extension (Client/Frontend)**: The user-facing component built with JavaScript, HTML, and CSS. Its primary responsibility is to detect a successful LeetCode submission and make a single, authenticated API call to the Backend API service with the problem's identifier.
* **The FastAPI API Server (Backend/Business Logic Layer)**: The central nervous system of the application, developed in Python using FastAPI. It is responsible for all primary business logic, data processing, user authentication, score calculation, and dispatching events to the Discord Bot Service.
* **The Discord Bot Service (Notification Layer)**: A standalone microservice managing interactions with Discord. It runs a `discord.py` bot for handling commands and a concurrent FastAPI server to expose a secure internal API that listens for events from the Backend API Server.
* **The Scheduler (Automation Layer)**: A background job runner, implemented as a cron job, responsible for time-based automation like ending contests or triggering data cleanup.
* **The Data Persistence Layer (Database/Storage Layer)**: The system's long-term memory, using MongoDB Atlas. It communicates exclusively with the Backend API Server.

### 1.2. Data and Logic Flow: From 'Submission' to 'Notification'

The primary user journey of a successful problem submission flows as follows:

1.  **Event Trigger**: A user successfully submits a solution on leetcode.com.
2.  **Detection**: The browser extension's content script detects this success event.
3.  **Secure API Call**: The extension's background service worker initiates a secure API call to the Python Backend API (e.g., `POST /api/v1/submissions`).
4.  **Backend Verification and Processing**: The Backend API receives the request and validates the user's identity. It checks its MongoDB database for cached problem info. If missing or stale, it fetches data from LeetCode's GraphQL API. The backend calculates the score, writes the new submission to MongoDB, and updates the user's contest score.
5.  **Asynchronous Event Dispatch**: The Backend API sends a "fire-and-forget" event payload to the Discord Bot Service.
6.  **Real-time Notification**: The Discord Bot Service receives the event, formats a rich message, and sends it to the configured Discord channel.

### 1.3. Technology Stack Recommendation

| Component | Technology | Rationale |
| :--- | :--- | :--- |
| **Backend API** | FastAPI (Python) | High-performance, async support, automatic data validation and documentation. |
| **Discord Bot** | `discord.py` + FastAPI | Hybrid service combining real-time bot interactions with an internal API for receiving events. |
| **Scheduler** | Cron | Robust, simple, and reliable for triggering API endpoints at fixed intervals. |
| **Database** | MongoDB Atlas | Fully managed, scalable NoSQL document database with a flexible schema. |
| **Frontend UI** | Svelte | Modern UI compiler that produces highly optimized, minimal JavaScript for a fast user experience. |
| **Deployment** | Docker, Google Cloud Run | Containerization for consistency, with serverless for the API and a container service for the long-running bot. |