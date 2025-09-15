<script>
  import { onMount } from 'svelte';

  let username = '';
  let password = '';
  let errorMessage = '';
  
  let isLoggedIn = false;
  let loggedInUser = '';
  let monitorStatus = '';

  // When the popup opens, check if a token is already stored
  onMount(() => {
    chrome.storage.local.get(['token', 'username'], (result) => {
      if (result.token && result.username) {
        isLoggedIn = true;
        loggedInUser = result.username;
        console.log("User is already logged in.", result);
      }
    });
  });
  function handleStartMonitoring() {
    chrome.runtime.sendMessage({ action: "startMonitoring" }, (response) => {
      if (response) {
        console.log("Response from background:", response);
        monitorStatus = response.message;
        // The message will disappear after 3 seconds
        setTimeout(() => { monitorStatus = '' }, 3000);
      } else {
        monitorStatus = "Error sending message to background.";
      }
    });
  }

  async function handleLogin() {
    errorMessage = '';
    const formBody = new URLSearchParams({ username, password }).toString();

    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        },
        body: formBody
      });

      const data = await response.json();

      if (response.ok) {
        // Save the token and username to the extension's local storage
        chrome.storage.local.set({ 
          token: data.access_token,
          username: username 
        }, () => {
          console.log('Token and username saved successfully.');
          isLoggedIn = true;
          loggedInUser = username;
        });
      } else {
        errorMessage = data.detail || 'Login failed.';
      }
    } catch (error) {
      console.error('Login error:', error);
      errorMessage = 'Could not connect to the server.';
    }
  }

  function handleLogout() {
    chrome.storage.local.remove(['token', 'username'], () => {
      isLoggedIn = false;
      loggedInUser = '';
      console.log('User logged out and token removed.');
    });
  }
</script>

<main>
  <h1>Social LeetCode</h1>

  {#if isLoggedIn}
    <div class="welcome-message">
      <p>Welcome, <strong>{loggedInUser}</strong>!</p>
      <button class="monitor-btn" on:click={handleStartMonitoring}>Start Monitoring</button>
      {#if monitorStatus}
        <p class="status-msg">{monitorStatus}</p>
      {/if}
      <button on:click={handleLogout}>Logout</button>
    </div>
    {:else}
    <form on:submit|preventDefault={handleLogin}>
      <div class="form-group">
        <label for="username">Username</label>
        <input type="text" id="username" bind:value={username} required />
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input type="password" id="password" bind:value={password} required />
      </div>
      <button type="submit">Login</button>
    </form>
    {#if errorMessage}
      <p class="error">{errorMessage}</p>
    {/if}
  {/if}
</main>

<style>
  main {
    font-family: sans-serif;
    text-align: center;
    padding: 1em;
    width: 300px;
  }
  .form-group { margin-bottom: 1rem; text-align: left; }
  label { display: block; margin-bottom: 0.25rem; }
  input { width: 100%; padding: 0.5rem; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px; }
  button { width: 100%; padding: 0.75rem; border: none; background-color: #007bff; color: white; border-radius: 4px; cursor: pointer; font-size: 1rem; }
  button:hover { background-color: #0056b3; }
  .welcome-message button { background-color: #dc3545; }
  .welcome-message button:hover { background-color: #c82333; }
  .error { color: red; margin-top: 1rem; }
  .welcome-message { margin-top: 1rem; }
  .monitor-btn {
    background-color: #28a745; /* Green */
    margin-bottom: 1rem;
  }
  .monitor-btn:hover {
    background-color: #218838;
  }
  .status-msg {
    font-size: 0.9rem;
    color: #555;
    margin-top: -0.5rem;
    margin-bottom: 1rem;
  }
</style>