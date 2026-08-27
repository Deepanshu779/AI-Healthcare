/**
 * MediAI 2.0 — Real-Time Conversational AI Health Assistant
 */

document.addEventListener("DOMContentLoaded", function () {
    const messagesStream = document.getElementById("chatMessagesStream");
    const chatInput = document.getElementById("chatInput");
    const sendBtn = document.getElementById("chatSendBtn");
    const suggestionChips = document.querySelectorAll(".suggestion-chip");

    if (!messagesStream || !chatInput) return;

    let conversationHistory = [];

    // Markdown simple parser for AI responses
    function formatMarkdown(text) {
        let html = text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`(.*?)`/g, '<code>$1</code>')
            .replace(/### (.*?)\n/g, '<h4 style="margin: 8px 0 4px; color: var(--primary);">$1</h4>')
            .replace(/## (.*?)\n/g, '<h3 style="margin: 10px 0 6px; color: var(--primary);">$1</h3>')
            .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" style="color: var(--primary); text-decoration: underline;">$1</a>')
            .replace(/\n\n/g, '<br><br>')
            .replace(/\n- /g, '<br>• ');
        return html;
    }

    function appendMessage(role, content) {
        const row = document.createElement("div");
        row.className = `chat-message-row ${role}`;

        const bubble = document.createElement("div");
        bubble.className = "msg-bubble";

        if (role === "bot") {
            bubble.innerHTML = formatMarkdown(content);
        } else {
            bubble.textContent = content;
        }

        row.appendChild(bubble);
        messagesStream.appendChild(row);
        messagesStream.scrollTop = messagesStream.scrollHeight;
    }

    function showTypingIndicator() {
        const row = document.createElement("div");
        row.className = "chat-message-row bot typing-indicator-row";
        row.id = "typingIndicator";

        const bubble = document.createElement("div");
        bubble.className = "msg-bubble";
        bubble.innerHTML = '<span class="typing-dots"><span>.</span><span>.</span><span>.</span></span>';

        row.appendChild(bubble);
        messagesStream.appendChild(row);
        messagesStream.scrollTop = messagesStream.scrollHeight;
    }

    function removeTypingIndicator() {
        const indicator = document.getElementById("typingIndicator");
        if (indicator) indicator.remove();
    }

    async function handleSendMessage(messageText) {
        const text = messageText || chatInput.value.trim();
        if (!text) return;

        // Append user message
        appendMessage("user", text);
        conversationHistory.push({ role: "user", content: text });
        chatInput.value = "";

        showTypingIndicator();

        try {
            const response = await fetch("/api/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ messages: conversationHistory })
            });

            removeTypingIndicator();

            if (!response.ok) {
                throw new Error("Network response was not ok");
            }

            const data = await response.json();
            const botResponse = data.response || "I apologize, but I was unable to process your request. Please try again.";
            appendMessage("bot", botResponse);
            conversationHistory.push({ role: "assistant", content: botResponse });

        } catch (error) {
            removeTypingIndicator();
            appendMessage("bot", "⚠️ Unable to connect to clinical intelligence engine. Please check your connection and try again.");
            console.error("Chat error:", error);
        }
    }

    if (sendBtn) {
        sendBtn.addEventListener("click", () => handleSendMessage());
    }

    chatInput.addEventListener("keydown", function (e) {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    });

    suggestionChips.forEach(chip => {
        chip.addEventListener("click", function () {
            const prompt = chip.dataset.prompt || chip.textContent.trim();
            handleSendMessage(prompt);
        });
    });
});
