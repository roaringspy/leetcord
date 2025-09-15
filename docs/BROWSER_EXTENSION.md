# Browser Extension Documentation

The browser extension is the primary user-facing client for LeetCord. It's built with Svelte and Vite for a fast, modern user experience.

## `manifest.json` Deep Dive

The `public/manifest.json` file is the core configuration of the extension.

-   **`"manifest_version": 3`**: Specifies the modern, secure Manifest V3 standard.
-   **`"permissions": ["storage", "debugger"]`**:
    -   `storage`: Grants access to `chrome.storage.local`, used for securely storing the user's JWT authentication token.
    -   `debugger`: Grants access to the `chrome.debugger` API, which is essential for our network interception strategy.
-   **`"host_permissions": ["*://*.leetcode.com/*"]`**: A critical security setting that restricts the extension's capabilities to only run on LeetCode web pages.
-   **`"background": { "service_worker": "background.js" }`**: Registers our main background script, which handles all core logic.
-   **`"action": { "default_popup": "index.html" }`**: Defines that when the user clicks the extension's icon in the toolbar, our Svelte application (`index.html`) should be displayed as a popup.

## State Management (`chrome.storage.local`)

The user's session (JWT token and username) is managed using `chrome.storage.local`. This provides a persistent, asynchronous storage mechanism that is sandboxed to the extension for security.

-   **Saving Data**: After a successful login, the token is saved using `chrome.storage.local.set({ token: '...', username: '...' })`.
-   **Retrieving Data**: When the popup opens, the `onMount` lifecycle function in `App.svelte` calls `chrome.storage.local.get(['token', 'username'], ...)` to check for an existing session and update the UI accordingly.

## Submission Detection Logic (`background.js`)

Detecting a successful submission reliably is the extension's most critical task. We use the `chrome.debugger` API for network interception, as it is vastly more reliable than observing page content (DOM) changes.

The process works as follows:
1.  **User Activation**: The user clicks a "Start Monitoring" button in the popup, which sends a message (`chrome.runtime.sendMessage`) to the background script. This attaches the debugger to the active LeetCode tab. An automatic listener on `chrome.tabs.onUpdated` also serves as a backup.
2.  **Enable Network Monitoring**: The script sends the `Network.enable` command to the debugger.
3.  **Listen for Events**: An event listener (`chrome.debugger.onEvent`) is set up to monitor all network activity on the page.
4.  **Track Requests**: The listener watches for two key events to prevent race conditions:
    -   `Network.responseReceived`: To identify when a request to LeetCode's submission check URL is made and to log its `requestId`.
    -   `Network.loadingFinished`: To ensure the full response body has been downloaded before we try to read it.
5.  **Get Response Body**: Once a tracked request is finished, the `Network.getResponseBody` command is used to retrieve the JSON content of the response.
6.  **Check for Success**: The JSON is parsed, and the script checks if `data.status_code === 10` and `data.run_success === true`.
7.  **Parse URL for Slug**: If successful, the script gets the details of the current tab using `chrome.tabs.get()` and parses the problem's unique name (the `title_slug`) from the tab's URL.
8.  **Call the Backend**: Finally, the script retrieves the stored JWT token from `chrome.storage.local` and makes an authenticated `fetch` call to our backend's `/api/v1/submissions` endpoint with the `title_slug`.

## UI Component (`App.svelte`)

The entire popup UI is managed within a single Svelte component, `src/App.svelte`.

-   **Conditional Rendering**: The UI uses Svelte's `{#if isLoggedIn}` block to show either the login form or a welcome message with the "Start Monitoring" and "Logout" buttons.
-   **State Management**: Local component state (e.g., `isLoggedIn`, `username`) is used to control what is displayed on the screen.
-   **Event Handling**: User actions like button clicks (`on:click`) or form submissions (`on:submit`) trigger JavaScript functions that handle API calls and communication with the background script.