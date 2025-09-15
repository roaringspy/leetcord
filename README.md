# LeetCord

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

A full-stack browser extension designed to create a social and competitive layer on top of LeetCode by integrating it with Discord. This project allows users to form groups, compete in contests, and get real-time notifications of friends' accepted submissions.

## Core Features (Current)

- **User Authentication**: Secure user registration and login system using JWT.
- **Submission Detection**: Reliably detects successful LeetCode submissions in real-time using the `chrome.debugger` API.
- **Real-time Discord Notifications**: A dedicated microservice sends formatted notifications to a Discord channel upon a successful submission.
- **Persistent Sessions**: The browser extension securely stores the user's login session.
- **Microservice Architecture**: The backend is designed as a system of decoupled services for scalability and robustness.

## Technology Stack

The project is built with a modern, high-performance technology stack.

| Area                | Technology                                                                          |
| ------------------- | ----------------------------------------------------------------------------------- |
| **Backend API** | Python, FastAPI, Uvicorn                                                            |
| **Database** | MongoDB Atlas (NoSQL Document Store)                                     |
| **Frontend** | Svelte, Vite, JavaScript                                                            |
| **Discord Bot** | `discord.py`, FastAPI (Hybrid Service)                                   |
| **Containerization**| Docker (for future deployment)                                             |

## Project Structure

This project is a monorepo containing the two main services:

```
.
├── backend/      # FastAPI server for the main API and Discord bot
└── frontend/     # Svelte project for the browser extension
```

## Getting Started: Setup and Installation

Follow these instructions to get the development environment running.

### Prerequisites

- [Git](https://git-scm.com/)
- [Python 3.9+](https://www.python.org/)
- [Node.js 18+](https://nodejs.org/) with npm
- A [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) account
- A [Discord](https://discord.com/) account and a server you can manage

### 1. Backend Setup

```bash
# Navigate to the backend directory
cd backend

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt # (You will need to create this file, see below)
```
**Create `backend/requirements.txt`:**
```txt
fastapi[all]
motor
httpx
python-dotenv
passlib[bcrypt]
python-jose[cryptography]
discord.py
email-validator
```

**Create Backend Environment Files:**
- In the `backend` folder, create a `.env` file and a `.env.discord` file.
- **Never commit these files to Git.**

**File: `backend/.env.example`** (Create this file to show what's needed)
```env
MONGO_DETAILS="mongodb+srv://<username>:<password>@<your-atlas-cluster>.mongodb.net/"
SECRET_KEY="<generate_a_strong_secret_key>"
DISCORD_BOT_URL="[http://127.0.0.1:8001](http://127.0.0.1:8001)"
```

**File: `backend/.env.discord.example`** (Create this file too)
```env
DISCORD_BOT_TOKEN="<your_bot_token_from_discord_dev_portal>"
NOTIFICATION_CHANNEL_ID="<your_discord_channel_id>"
```

**Run the Backend:**
- You will need two terminals.
- **Terminal 1:** `uvicorn main:app --reload`
- **Terminal 2:** `python discord_bot.py`

### 2. Frontend Setup

```bash
# Navigate to the frontend directory from the root
cd frontend

# Install Node.js dependencies
npm install
```
**Note**: When you first create the frontend project with `npm create vite@latest`, you can name the internal project `leetcord-extension`.

**Create Frontend Configuration:**
- In the `frontend` folder, create a `jsconfig.json` file to enable editor support for the `chrome` API.

**File: `frontend/jsconfig.json`**
```json
{
  "compilerOptions": {
    "target": "ESNext",
    "module": "ESNext",
    "types": ["svelte", "chrome"]
  },
  "include": ["src/**/*"]
}
```

**Run and Load the Extension:**
1.  Run the dev server: `npm run dev`
2.  Open your browser to `chrome://extensions`.
3.  Enable "Developer mode".
4.  Click "Load unpacked" and select the `frontend/dist` folder.

## Project Roadmap

This project is under active development. Our vision includes the following features:
- **Enhanced Scoring System**: Implement a more complex and configurable scoring algorithm.
- **Google OAuth**: Allow users to sign up and log in using their Google accounts.
- **Friends System**: Implement functionality for users to add and manage friends.
- **Leaderboards**: Create detailed leaderboards for different contests and timeframes.
- **Contest Management**: Build out the scheduler and API endpoints for creating and managing contests.
- **UI/UX Overhaul**: Redesign the extension popup for a more polished user experience.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License.