/* ==========================================================
   AI Healthcare Diagnosis Assistant
   Frontend Controller
========================================================== */

const input = document.getElementById("userInput");

const sendBtn = document.getElementById("sendBtn");

const chatBody = document.getElementById("chatBody");

const typingIndicator = document.getElementById("typingIndicator");

const welcomeScreen = document.getElementById("welcomeScreen");

const newChatBtn = document.getElementById("newChatBtn");

const suggestions = document.querySelectorAll(".suggestion");

// Store current chat session
let currentConversation = [];


/* ==========================================================
   Create Chat Bubble
========================================================== */

function createMessage(text, sender) {

    const message = document.createElement("div");

    message.className = `message ${sender}`;

    const content = document.createElement("div");

    content.className = "message-content";

    content.innerHTML = text;

    message.appendChild(content);

    chatBody.appendChild(message);

    scrollToBottom();

    return content;

}



/* ==========================================================
   Auto Scroll
========================================================== */

function scrollToBottom() {

    chatBody.scrollTop = chatBody.scrollHeight;

}


/* ==========================================================
   Greeting Detection
========================================================== */

function isGreeting(text) {

    const greetings = [
        "hi",
        "hello",
        "hey",
        "how are you",
        "who are you",
        "what is your name",
        "good morning",
        "good afternoon",
        "good evening",
        "thanks",
        "thank you",
        "bye",
        "goodbye",
        "good night",
        "ok",
        "okay"
    ];

    const message = text.trim().toLowerCase();

    return greetings.some(greeting => message.includes(greeting));
}



/* ==========================================================
   Typing Indicator
========================================================== */



const typingStatus = document.getElementById("typingStatus");

const loadingSteps = [

    "Searching medical knowledge...",

    "Retrieving relevant context...",

    "Generating AI response..."

];

let loadingIndex = 0;

let loadingInterval;

function showTyping() {

    typingIndicator.classList.add("show");

    typingStatus.innerText = loadingSteps[0];

    loadingInterval = setInterval(() => {

        loadingIndex++;

        if (loadingIndex >= loadingSteps.length) {

            loadingIndex = 0;

        }

        typingStatus.innerText = loadingSteps[loadingIndex];

    }, 1200);

    scrollToBottom();

}

function hideTyping() {

    clearInterval(loadingInterval);

    typingIndicator.classList.remove("show");

}


/* ==========================================================
   Send Message
========================================================== */

async function sendMessage() {

    const question = input.value.trim();

    if (question === "") return;

    welcomeScreen.style.display = "none";

    createMessage(question, "user");

if (!isGreeting(question)) {

    currentConversation.push({
        role: "user",
        message: question
    });

}

    input.value = "";

    input.focus();

    if (isGreeting(question)) {

    const replies = {
    "hi": "Hello! 👋 How can I help you with your health today?",
    "hello": "Hello! 👋 How can I assist you today?",
    "hey": "Hi! 😊 What health concern can I help you with?",

    "how are you": "I'm doing well, thank you! 😊 I'm here and ready to help with any health-related questions you have.",

    "who are you": "I'm VitaCare AI, your healthcare assistant. I can help answer medical questions and provide general health information.",

    "what is your name": "I'm VitaCare AI, your healthcare assistant.",

    "good morning": "Good morning! ☀️ How can I help you today?",
    "good afternoon": "Good afternoon! 😊 How can I assist you today?",
    "good evening": "Good evening! 🌙 How can I help you today?",
    "thanks": "You're welcome! 😊 Wishing you good health.",
    "thank you": "You're welcome! 😊 Wishing you good health.",
    "bye": "Goodbye! 👋 Take care and stay healthy.",
    "goodbye": "Goodbye! 👋 Take care and stay healthy.",
    "good night": "Good night! 🌙 Take care."
};

    const lower = question.trim().toLowerCase();

    const matched = Object.keys(replies).find(key => lower.includes(key));

    createMessage(
    replies[matched] || "Hello! 👋 How can I help you today?",
    "ai"
);

    return;
}

showTyping();

await getAIResponse(question);

}

/* ==========================================================
   Get AI Response
========================================================== */

async function getAIResponse(question) {

    input.disabled = true;
    sendBtn.disabled = true;

    try {

        const response = await fetch("/stream", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: question
            })
        });
        
        if (!response.ok) {
            throw new Error(`Server Error: ${response.status}`);
        }
        
        hideTyping();

        const reader = response.body.getReader();

        const decoder = new TextDecoder();

        const aiMessage = createMessage("", "ai");
        let completeAnswer = "";

        while (true) {

            const { done, value } = await reader.read();

            if (done) break;

            const chunk = decoder.decode(value);
            completeAnswer += chunk;
            
            aiMessage.innerHTML += chunk;
            
            scrollToBottom();
        }
        
        if (!isGreeting(question)) {

    currentConversation.push({
        role: "assistant",
        message: completeAnswer
    });

    console.log("Current Conversation:", currentConversation);
}

input.disabled = false;
sendBtn.disabled = false;


}
    
    
catch (error) {

    hideTyping();

    input.disabled = false;
    sendBtn.disabled = false;

    console.error("Streaming Error:", error);

    createMessage(
        "⚠️ " + error.message,
        "ai"
    );

}

}

/* ==========================================================
   Enter Key
========================================================== */

input.addEventListener("keypress", function(event){

    if(event.key==="Enter"){

        event.preventDefault();

        sendMessage();

    }

});


/* ==========================================================
   Send Button
========================================================== */

sendBtn.addEventListener("click", function(){

    sendMessage();

});


/* ==========================================================
   Suggestions
========================================================== */

suggestions.forEach(button=>{

    button.addEventListener("click",()=>{

        input.value=button.innerText;

        input.focus();

    });

});


/* ==========================================================
   New Chat
========================================================== */

newChatBtn.addEventListener("click", () => {

    if (currentConversation.length > 0) {

        if (!confirm("Start a new chat? Unsaved consultation will be lost.")) {
            return;
        }

    }

    chatBody.innerHTML = "";

    welcomeScreen.style.display = "flex";

    currentConversation = [];

    input.value = "";

    input.focus();

});

/* ==========================================================
   Save Consultation
========================================================== */

const saveBtn = document.getElementById("saveConversationBtn");

saveBtn.addEventListener("click", async () => {

    // Remove greetings before saving
    const conversationToSave = currentConversation.filter(message =>
        !isGreeting(message.message)
    );

    if (conversationToSave.length === 0) {
        alert("No medical consultation available to save.");
        return;
    }

    try {

        const response = await fetch("/save-consultation", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                conversation: conversationToSave
            })

        });

        const data = await response.json();

        alert(data.message);

    } catch (error) {

        console.error(error);

        alert("Unable to save consultation.");

    }

});


/* ==========================================================
   Clear Chat
========================================================== */

const clearBtn = document.getElementById("clearChatBtn");

clearBtn.addEventListener("click", () => {

    if (!confirm("Clear the current chat?")) {
        return;
    }

    chatBody.innerHTML = "";

    welcomeScreen.style.display = "flex";

    currentConversation = [];

    input.value = "";

    input.focus();

});

