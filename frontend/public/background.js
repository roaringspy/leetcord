console.log("Social LeetCode background script loaded.");

const LEETCODE_SUBMISSION_URL_PATTERN = "https://leetcode.com/submissions/detail/";
const attachedTabs = new Set();
const requests = {};

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "startMonitoring") {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs[0] && tabs[0].id) {
        const tabId = tabs[0].id;
        if (tabs[0].url && tabs[0].url.includes("leetcode.com/problems/")) {
          if (!attachedTabs.has(tabId)) {
            attachedTabs.add(tabId);
            attachDebugger(tabId);
            sendResponse({ status: "success", message: `Debugger attached to tab ${tabId}` });
          } else {
            sendResponse({ status: "already_attached", message: `Debugger is already attached to tab ${tabId}` });
          }
        } else {
          sendResponse({ status: "error", message: "Not a LeetCode problem page." });
        }
      }
    });
    return true; 
  }
});

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status !== 'complete') { return; }
  if (tab.url && tab.url.includes("leetcode.com/problems/") && !attachedTabs.has(tabId)) {
    attachedTabs.add(tabId); 
    attachDebugger(tabId);
  }
});

function attachDebugger(tabId) {
  const version = "1.3";
  chrome.debugger.attach({ tabId: tabId }, version, () => {
    if (chrome.runtime.lastError) {
      console.error(chrome.runtime.lastError.message);
      attachedTabs.delete(tabId); 
      return;
    }
    console.log(`Debugger attached to tab ${tabId}.`);
    chrome.debugger.onDetach.addListener((source, reason) => {
      if (source.tabId === tabId) {
        console.log(`Debugger detached from tab ${tabId}. Reason: ${reason}`);
        attachedTabs.delete(tabId);
      }
    });
    chrome.debugger.sendCommand({ tabId: tabId }, "Network.enable", {}, () => {
      if (chrome.runtime.lastError) { console.error(chrome.runtime.lastError.message); } 
      else { console.log("Network monitoring enabled."); }
    });
  });
}

chrome.debugger.onEvent.addListener((source, method, params) => {
  if (method === "Network.responseReceived" && params.response.url.includes(LEETCODE_SUBMISSION_URL_PATTERN)) {
    requests[params.requestId] = { url: params.response.url };
  }

  if (method === "Network.loadingFinished" && requests[params.requestId]) {
    chrome.debugger.sendCommand(
      { tabId: source.tabId },
      "Network.getResponseBody",
      { requestId: params.requestId },
      (responseBody) => {
        delete requests[params.requestId];
        if (chrome.runtime.lastError) { return; }

        if (responseBody && responseBody.body) {
          try {
            const data = JSON.parse(responseBody.body);
            // FINAL, CORRECTED LOGIC
            if (data.status_code === 10 && data.run_success === true) {
              console.log("SUCCESS! Submission Accepted:", data);
              // We don't have the problem slug here, so we pass the tabId to the handler
              handleSuccessfulSubmission(source.tabId); 
            }
          } catch (e) {
            // This can be ignored, as it's likely just parsing a pending state
          }
        }
      }
    );
  }
});

// COMPLETELY REWRITTEN FUNCTION
function handleSuccessfulSubmission(tabId) {
  // Step 1: Get the details of the tab to find its URL
  chrome.tabs.get(tabId, (tab) => {
    if (chrome.runtime.lastError || !tab) {
      console.error("Could not get tab details.");
      return;
    }

    // Step 2: Parse the problem slug from the tab's URL
    // e.g., "https://leetcode.com/problems/two-sum/" -> "two-sum"
    const urlParts = tab.url.split('/');
    const problemsIndex = urlParts.indexOf('problems');
    if (problemsIndex === -1 || urlParts.length <= problemsIndex + 1) {
      console.error("Could not parse problem slug from URL:", tab.url);
      return;
    }
    const problemSlug = urlParts[problemsIndex + 1];

    // Step 3: Get the saved user token
    chrome.storage.local.get(['token'], (result) => {
      if (result.token) {
        console.log(`Sending successful submission for '${problemSlug}' to our backend.`);
        const submissionData = {
          problem_slug: problemSlug,
          contest_id: "default-contest"
        };

        // Step 4: Make the authenticated API call to our backend
        fetch('http://127.0.0.1:8000/api/v1/submissions', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${result.token}`
          },
          body: JSON.stringify(submissionData)
        })
        .then(response => response.json())
        .then(data => {
          if (data.detail) {
            console.error("Backend submission error:", data.detail);
          } else {
            console.log("Backend successfully recorded submission:", data);
          }
        })
        .catch(error => {
          console.error("Error sending submission to backend:", error);
        });
      } else {
        console.log("User is not logged in. Cannot record submission.");
      }
    });
  });
}