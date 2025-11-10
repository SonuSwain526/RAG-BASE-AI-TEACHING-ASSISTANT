// Add event listener for "Enter" key
document.getElementById("user-input").addEventListener("keypress", function(event) {
  if (event.key === "Enter") {
    event.preventDefault(); // Stop default form submit
    sendQuestion();
  }
});

async function sendQuestion() {
  const input = document.getElementById("user-input");
  const question = input.value.trim();
  if (!question) return;

  appendMessage("user", question);
  input.value = "";
  showTypingIndicator();

  try {
    const res = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });
    
    if (!res.ok) {
        throw new Error(`Server error: ${res.status}`);
    }

    const data = await res.json();
    
    hideTypingIndicator();
    appendMessage("bot", data.answer);

  } catch (error) {
    hideTypingIndicator();
    appendMessage("bot", `Sorry, I ran into an error: ${error.message}`);
    console.error("Error fetching response:", error);
  }
}

function appendMessage(sender, text) {
  const box = document.getElementById("chat-box");
  const msg = document.createElement("div");
  msg.classList.add("message", sender);
  
  // Basic markdown-like formatting for newlines
  msg.innerHTML = text.replace(/\n/g, '<br>');
  
  box.appendChild(msg);
  box.scrollTop = box.scrollHeight;
}

function showTypingIndicator() {
  const box = document.getElementById("chat-box");
  const typingMsg = document.createElement("div");
  typingMsg.id = "typing-indicator";
  typingMsg.classList.add("message", "bot", "typing-indicator");
  typingMsg.innerHTML = `
    <span></span>
    <span></span>
    <span></span>
  `;
  box.appendChild(typingMsg);
  box.scrollTop = box.scrollHeight;
}

function hideTypingIndicator() {
  const indicator = document.getElementById("typing-indicator");
  if (indicator) {
    indicator.remove();
  }
}