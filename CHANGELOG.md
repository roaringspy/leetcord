# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
-   Project `TODO.md` and `CHANGELOG.md` for project management.
-   Detailed documentation for Architecture, Backend API, Discord Bot, and Browser Extension.

## [1.0.0] - 2025-09-16

### Added
-   **Initial Foundation Release**
-   **Backend**: FastAPI server with JWT-based user registration (`/register`) and login (`/login`).
-   **Backend**: Secure password hashing with `bcrypt`.
-   **Backend**: API endpoint (`/submissions`) to record successful LeetCode submissions.
-   **Backend**: Service to cache LeetCode problem details from the public GraphQL API.
-   **Backend**: CORS middleware to allow communication from the browser extension.
-   **Discord Bot**: Standalone microservice using `discord.py` and FastAPI.
-   **Discord Bot**: Listens for events from the backend and posts formatted embed messages for new submissions.
-   **Browser Extension**: Svelte and Vite-based popup UI.
-   **Browser Extension**: Persistent user login state using `chrome.storage.local`.
-   **Browser Extension**: Robust submission detection using the `chrome.debugger` API for network interception.
-   **Browser Extension**: Manual "Start Monitoring" button for reliable debugger attachment.
-   **Version Control**: Project initialized on GitHub with a monorepo structure and `.gitignore`.