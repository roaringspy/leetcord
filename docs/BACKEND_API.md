# Backend API Documentation

The backend is the core of the LeetCord application, handling all business logic, data persistence, and security. It is built with Python using the high-performance **FastAPI** framework.

## Table of Contents
1.  [Authentication Flow](#authentication-flow)
2.  [Database Models](#database-models)
3.  [API Endpoint Specification](#api-endpoint-specification)
    -   [POST /api/v1/auth/register](#post-apiv1authregister)
    -   [POST /api/v1/auth/login](#post-apiv1authlogin)
    -   [POST /api/v1/submissions](#post-apiv1submissions)
4.  [CORS Configuration](#cors-configuration)

---

## Authentication Flow

Authentication is handled using the **OAuth2 "Password Flow"** with **JWT Bearer Tokens**.

#### 1. Obtaining a Token
A client must first authenticate by sending a user's credentials (username and password) to the `/api/v1/auth/login` endpoint. If the credentials are valid, the server returns a signed JWT `access_token`.

#### 2. Using a Token
For all requests to protected endpoints, the client must include this token in the `Authorization` header. The server will reject any request to a protected route that does not include a valid token.

- **Header Format**: `Authorization: Bearer <your_jwt_access_token>`

#### 3. Token Expiration
Tokens are configured to expire after a set period (e.g., 30 minutes) for security. After expiration, the user must log in again to obtain a new token.

---

## Database Models

Data is stored in a MongoDB Atlas database, organized into the following collections.

### `users` Collection
Stores user account information. Passwords are never stored in plain text; they are securely hashed using **bcrypt**.

| Field | Type | Description |
|---|---|---|
| `_id` | ObjectId | Unique identifier for the user. |
| `username` | String | Unique username for login. |
| `email` | String | User's email address. |
| `hashed_password` | String | The bcrypt-hashed password. |

### `problems` Collection
Caches data for LeetCode problems to reduce external API calls and improve performance.

| Field | Type | Description |
|---|---|---|
| `_id` | ObjectId | Unique identifier for the cached problem. |
| `title_slug` | String | The unique URL-friendly name (e.g., "two-sum"). |
| `title` | String | The display title (e.g., "Two Sum"). |
| `difficulty` | String | "Easy", "Medium", or "Hard". |
| `acceptance_rate`| Float | The problem's acceptance rate at the time of caching. |
| `last_updated` | DateTime | Timestamp of the last cache update. |

### `submissions` Collection
A historical log of all successful submissions recorded by the extension.

| Field | Type | Description |
|---|---|---|
| `_id` | ObjectId | Unique identifier for the submission record. |
| `user_id` | String | The ObjectId (as a string) of the user who made the submission. |
| `problem_id` | ObjectId | Reference to the `_id` in the `problems` collection. |
| `contest_id` | String | Identifier for the contest the submission belongs to. |
| `score` | Integer | The score awarded for this submission based on difficulty. |
| `submitted_at` | DateTime | Timestamp of when the submission was recorded. |

---

## API Endpoint Specification

### POST /api/v1/auth/register
Registers a new user account.

- **Authentication**: `Public`
- **Request Headers**:
  - `Content-Type: application/json`

- **Request Body**:
  | Field | Type | Description | Required |
  |---|---|---|---|
  | `username` | String | The desired username. Must be unique. | Yes |
  | `email` | String | A valid email address. | Yes |
  | `password` | String | The desired password. | Yes |
  
  **Example:**
  ```json
  {
    "username": "newuser",
    "email": "user@example.com",
    "password": "strongpassword123"
  }

  - **Responses**:
      - **`200 OK` (Success)**: The user was created successfully. The response body contains the public user data.
        ```json
        {
          "_id": "68c8707f5b0c22352be7aaab",
          "username": "newuser",
          "email": "user@example.com"
        }
        ```
      - **`400 Bad Request` (Error)**: The username is already taken.
        ```json
        {
          "detail": "Username already registered"
        }
        ```

### POST /api/v1/auth/login

Authenticates a user and returns a JWT access token.

  - **Authentication**: `Public`

  - **Request Headers**:

      - `Content-Type: application/x-www-form-urlencoded`

  - **Request Body**:
    | Field | Type | Description | Required |
    |---|---|---|---|
    | `username` | String | The user's username. | Yes |
    | `password` | String | The user's password. | Yes |

    **Example:**

    ```
    username=newuser&password=strongpassword123
    ```

  - **Responses**:

      - **`200 OK` (Success)**: Authentication was successful.
        ```json
        {
          "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
          "token_type": "bearer"
        }
        ```
      - **`401 Unauthorized` (Error)**: The username or password was incorrect.
        ```json
        {
          "detail": "Incorrect username or password"
        }
        ```

### POST /api/v1/submissions

Records a new successful problem submission for the authenticated user.

  - **Authentication**: `Bearer Token Required`

  - **Request Headers**:

      - `Content-Type: application/json`
      - `Authorization: Bearer <your_jwt_access_token>`

  - **Request Body**:
    | Field | Type | Description | Required |
    |---|---|---|---|
    | `problem_slug` | String | The unique URL-friendly name of the problem. | Yes |
    | `contest_id` | String | The identifier for the current contest. | Yes |

    **Example:**

    ```json
    {
      "problem_slug": "two-sum",
      "contest_id": "default-contest"
    }
    ```

  - **Responses**:

      - **`200 OK` (Success)**: The submission was recorded successfully. The response contains the created submission document.
        ```json
        {
          "_id": "68c8755dc3f1bfe19b3a9099",
          "user_id": "68c8707f5b0c22352be7aaab",
          "problem_id": "68c8755d2a02a212221126b2",
          "contest_id": "default-contest",
          "score": 10,
          "submitted_at": "2025-09-15T20:21:49.617000"
        }
        ```
      - **`401 Unauthorized` (Error)**: The provided JWT token is missing, invalid, or expired.
        ```json
        {
          "detail": "Could not validate credentials"
        }
        ```
      - **`404 Not Found` (Error)**: The `problem_slug` does not correspond to a known LeetCode problem.
        ```json
        {
          "detail": "Problem 'invalid-slug' not found on LeetCode."
        }
        ```

-----

## CORS Configuration

The backend is configured with FastAPI's `CORSMiddleware` to allow cross-origin requests from the browser extension. For development, `allow_origins` is set to `["*"]` to simplify testing. For a production deployment, this should be restricted to the specific origin of the published browser extension for enhanced security.