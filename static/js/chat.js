// Grab the textarea where the user types their prompt
const promptInput = document.getElementById("prompt");

// Grab the button that triggers sending a message
const sendBtn = document.getElementById("send-btn");

// Grab the container element where chat messages (user and AI) will be appended
const chat = document.getElementById("chat");

// Grab the button that allows starting a new chat session
const newChatBtn = document.getElementById("new-chat");

// ------------------ UUID / Session Setup ------------------

// Function to generate a universally unique identifier (UUID v4) for tracking the chat session
// Uses crypto.getRandomValues to ensure high-quality randomness
function generateUUID() {
  return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
    (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
  );
}

// Try to get a stored session ID from localStorage to maintain chat continuity
let sessionId = localStorage.getItem("session_id");

// If no session ID exists, generate a new one and store it for future use
if (!sessionId) {
  sessionId = generateUUID();
  localStorage.setItem("session_id", sessionId);
}

// ------------------ Auto-grow Textarea ------------------

// Function to automatically adjust the height of the textarea based on its content
// Prevents scrollbars and provides a smooth typing experience
function autoGrowTextarea() {
  promptInput.style.height = "auto"; // Reset height to allow shrinking if content is deleted
  promptInput.style.height = promptInput.scrollHeight + "px"; // Set height to match content
}

// Attach the auto-grow functionality to the textarea input event
promptInput.addEventListener("input", autoGrowTextarea);

// ------------------ Markdown-it Setup ------------------

// Initialize Markdown rendering library (markdown-it) if available
// Fallback to a simple pass-through function if markdown-it is not loaded
const md = window.markdownit?.() || { render: t => t };

// ------------------ Send Message ------------------

// Asynchronous function to handle sending messages from the user to the AI and displaying responses
async function sendMessage() {
  // Get the trimmed text from the input field
  const text = promptInput.value.trim();

  // Do nothing if input is empty or if the send button is currently disabled
  if (!text || sendBtn.disabled) return;

  // ------------------ Append User Message ------------------

  // Create a new div element to represent the user's message
  const userDiv = document.createElement("div");
  userDiv.className = "message user"; // Apply styling for user messages
  userDiv.textContent = text; // Set the message content
  chat.appendChild(userDiv); // Append user message to chat container

  // Clear the input and adjust the textarea height after sending
  promptInput.value = "";
  autoGrowTextarea();

  // ------------------ Append AI Placeholder ------------------

  // Create a new div element for the AI response
  // Initially shows a typing indicator while the AI response is being fetched
  const aiDiv = document.createElement("div");
  aiDiv.className = "message ai"; // Apply styling for AI messages
  aiDiv.innerHTML = "<span class='typing-indicator'><span></span><span></span><span></span></span>";
  chat.appendChild(aiDiv); // Append AI placeholder to chat container

  // Disable the send button and add a loading class while awaiting response
  sendBtn.classList.add("loading");
  sendBtn.disabled = true;

  // Scroll the chat container so the AI placeholder is visible
  aiDiv.scrollIntoView({ behavior: "smooth", block: "start" });

  try {
    // Send the user prompt and session ID to the server endpoint /chat using POST
    const response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt: text, session_id: sessionId })
    });

    // Read the server response as a stream to support live updates
    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let aiContent = "";

    // Remove the typing indicator immediately before receiving actual AI content
    aiDiv.innerHTML = "";

    // Stream the AI response chunk by chunk
    while (true) {
      const { done, value } = await reader.read();
      if (done) break; // Exit loop when response is complete

      // Decode the chunk and append to accumulated AI content
      const chunk = decoder.decode(value, { stream: true });
      aiContent += chunk;

      // Render the accumulated AI content as Markdown in real-time
      aiDiv.innerHTML = md.render(aiContent);

      // Apply syntax highlighting for code blocks using Prism if available
      // The async flag allows highlighting large messages without blocking the UI
      if (window.Prism) Prism.highlightAll({ async: true });
    }
  } catch (err) {
    // Log any errors to the console and display an error message in the chat
    console.error("REAL ERROR:", err);
    aiDiv.textContent = "⚠️ " + err.message;
  } finally {
    // Remove loading state and re-enable the send button after AI response completes
    sendBtn.classList.remove("loading");
    sendBtn.disabled = false;
  }
}

// ------------------ Send Button & Enter Key ------------------

// Add click event listener to send button to trigger sending a message
sendBtn.addEventListener("click", sendMessage);

// Add keydown listener to allow sending a message by pressing Enter (without Shift)
// Prevent default newline behavior when pressing Enter alone
promptInput.addEventListener("keydown", e => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

// ------------------ New Chat ------------------

// Add click event listener to the New Chat button
// Sends a request to the server to start a fresh chat session
newChatBtn.addEventListener("click", async () => {
  try {
    // Retrieve the current session ID from localStorage to pass to server
    const oldSessionId = localStorage.getItem("session_id") || null;

    // Send POST request to /new_chat endpoint to create a new session
    const response = await fetch("/new_chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: oldSessionId })
    });

    // Parse the JSON response from the server
    const data = await response.json();

    // If the server confirms a new session, update session ID and reset the chat UI
    if (data.status === "ok") {
      sessionId = data.session_id; // Update local session ID
      localStorage.setItem("session_id", sessionId); // Store new session ID
      chat.innerHTML = ""; // Clear all chat messages
      promptInput.value = ""; // Clear input field
      autoGrowTextarea(); // Reset textarea height
    }
  } catch (err) {
    // Handle errors gracefully by logging and alerting the user
    console.error("Error starting new chat:", err);
    alert("Failed to start a new chat. Please try again.");
  }
});