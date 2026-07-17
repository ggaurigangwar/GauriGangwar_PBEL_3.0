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

    input.value = "";

    input.focus();

    showTyping();

    await getAIResponse(question);

}

/* ==========================================================
   Get AI Response
========================================================== */

async function getAIResponse(question) {

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

        hideTyping();

        const reader = response.body.getReader();

        const decoder = new TextDecoder();

        const aiMessage = createMessage("", "ai");

        while (true) {

            const { done, value } = await reader.read();

            if (done) break;

            aiMessage.innerHTML += decoder.decode(value);

            scrollToBottom();

        }

    }

    catch (error) {

    hideTyping();

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

newChatBtn.addEventListener("click",()=>{

    chatBody.innerHTML="";

    welcomeScreen.style.display="flex";

    input.value="";

    input.focus();

});

