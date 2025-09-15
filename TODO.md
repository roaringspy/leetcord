# LeetCord Project To-Do List

This document outlines the planned features and tasks for the LeetCord project. It serves as our development roadmap.

## Version 1.0 (Current Foundation)
- [x] **Backend API**: User authentication, problem caching, and submission tracking.
- [x] **Discord Bot**: Real-time notifications for successful submissions.
- [x] **Browser Extension**: Login, session management, and submission detection.
- [x] **Documentation**: Initial setup of README and detailed docs.
- [x] **Version Control**: Project setup on GitHub.

## Next Up: The Social & Competitive Features

### Friends System
-   [ ] **Backend**: Create `friendships` collection in MongoDB.
-   [ ] **Backend**: Develop API endpoint to send a friend request (`POST /friends/requests`).
-   [ ] **Backend**: Develop API endpoint to view pending requests (`GET /friends/requests`).
-   [ ] **Backend**: Develop API endpoint to accept/decline a request (`PUT /friends/requests/{id}`).
-   [ ] **Backend**: Develop API endpoint to list all friends (`GET /friends`).
-   [ ] **Backend**: Develop API endpoint to remove a friend (`DELETE /friends/{id}`).
-   [ ] **Frontend**: Create a new "Friends" tab in the extension popup.
-   [ ] **Frontend**: Build UI for searching users and sending requests.
-   [ ] **Frontend**: Build UI for managing incoming friend requests.
-   [ ] **Frontend**: Build UI to display the user's friends list.

### Scoring & Leaderboards
-   [ ] **Scoring System**: Design and implement an improved, configurable scoring algorithm (e.g., points based on acceptance rate, speed).
-   [ ] **User Points**: Add a `total_score` field to the `users` collection in MongoDB.
-   [ ] **Backend**: Create an aggregation pipeline to calculate and update user scores.
-   [ ] **Backend**: Develop API endpoint to get a global leaderboard (`GET /leaderboard/global`).
-   [ ] **Backend**: Develop API endpoint to get a friends-only leaderboard (`GET /leaderboard/friends`).
-   [ ] **Frontend**: Build UI for displaying leaderboards in the extension.

### User Experience & Authentication
-   [ ] **Google OAuth**: Implement "Sign in with Google" for both registration and login.
-   [ ] **UI Overhaul**: Redesign the extension popup for a more modern and intuitive look.
-   [ ] **Discord Bot Invite**: Create a simple flow or command for other server owners to invite the bot.

## Future Ideas
-   [ ] **Contest Management**: A system for creating, scheduling, and joining time-based contests.
-   [ ] **User Profiles**: Public profiles showing stats, recent submissions, and friends.
-   [ ] **Achievements**: A system for awarding badges or achievements for milestones.