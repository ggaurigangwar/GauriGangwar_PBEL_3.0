# 🩺 AI Healthcare Diagnosis Assistant

An AI-powered Healthcare Diagnosis Assistant built using **Flask**, **LangChain**, **Pinecone**, **Ollama (Llama 3)**, and **Retrieval-Augmented Generation (RAG)**. The application enables users to ask medical questions, receive AI-assisted responses based on a medical knowledge base, manage their health profile, and save consultation history.

> **Disclaimer:** This application is designed for educational and informational purposes only. It is **not** a substitute for professional medical advice, diagnosis, or treatment.

---

# 📌 Table of Contents

- Features
- Tech Stack
- System Architecture
- Project Structure
- Installation
- Configuration
- How to Run
- Application Workflow
- Screenshots
- Future Enhancements
- Author
- License

---

# ✨ Features

### 👤 User Management
- User Registration
- Secure Login & Logout
- Password Encryption using Bcrypt

### 🩺 Patient Profile
- Personal Health Profile
- Height & Weight
- Blood Group
- Existing Diseases
- Allergies
- Current Medications

### 🤖 AI Healthcare Chatbot
- AI-powered medical conversations
- Personalized responses using patient profile
- Context-aware healthcare assistance
- Medical knowledge retrieval using RAG

### 📚 Retrieval-Augmented Generation (RAG)
- Medical knowledge base
- HuggingFace Embeddings
- Pinecone Vector Database
- LangChain Retrieval Pipeline

### 💬 Consultation Management
- Save complete consultations
- View consultation history
- Medical question-based consultation titles

### ⚡ User Experience
- Streaming AI responses
- Modern responsive interface
- Greeting detection
- Interactive chat experience

---

# 🛠 Tech Stack

## Frontend

- HTML5
- CSS3
- JavaScript
- Bootstrap 5

## Backend

- Python
- Flask
- Flask Login
- SQLAlchemy
- SQLite

## Artificial Intelligence

- LangChain
- Ollama (Llama 3)
- Pinecone Vector Database
- HuggingFace Embeddings
- Retrieval-Augmented Generation (RAG)

---

# 🏗 System Architecture

```
                    User

                      │
                      ▼

             Flask Web Application

                      │
        ┌─────────────┴─────────────┐
        │                           │
        ▼                           ▼

 User Authentication         Patient Profile

                      │
                      ▼

             Chat Management

                      │
                      ▼

          Retrieval-Augmented Generation

          ┌────────────┴─────────────┐
          │                          │

     Pinecone Vector DB       Medical Knowledge Base

                      │
                      ▼

                Llama 3 (Ollama)

                      │
                      ▼

               AI Medical Response
```

---

# 📂 Project Structure

```
AI-Healthcare-Diagnosis-Assistant-Project/

│
├── app.py
├── models.py
├── extensions.py
├── requirements.txt
├── config.py
│
├── routes/
│   ├── auth.py
│   ├── chatbot.py
│   ├── dashboard.py
│   └── profile.py
│
├── src/
│   ├── agents/
│   ├── chat_manager.py
│   ├── helper.py
│   ├── memory.py
│   ├── prompt.py
│   └── response_formatter.py
│
├── static/
│   ├── css/
│   ├── js/
│   └── assets/
│
├── templates/
│
├── instance/
│
├── README.md
└── requirements.txt
```

---

# ⚙ Installation

## Clone the Repository

```bash
git clone https://github.com/ggaurigangwar/AI-Healthcare-Diagnosis-Assistant.git
```

## Navigate to Project

```bash
cd AI-Healthcare-Diagnosis-Assistant
```

## Create Virtual Environment

```bash
python -m venv .venv
```

## Activate Environment

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ⚙ Configuration

Create a `.env` file and configure your environment variables.

Example:

```env
PINECONE_API_KEY=YOUR_API_KEY
PINECONE_INDEX_NAME=medical-chatbot
```

Make sure:

- Ollama is installed
- Llama 3 model is downloaded
- Pinecone index is created
- HuggingFace embeddings are configured

---

# ▶ Run the Application

```bash
python app.py
```

Open your browser:

```
http://127.0.0.1:5000
```

---

# 🔄 Application Workflow

1. User registers or logs in.
2. User completes their health profile.
3. User asks a medical question.
4. Relevant medical documents are retrieved from Pinecone.
5. LangChain combines retrieved knowledge with the user's query.
6. Llama 3 generates a context-aware medical response.
7. User receives a streamed AI response.
8. Consultation can be saved and viewed later.


---


# 📚 Learning Outcomes

Through this project, I gained practical experience in:

- Flask Web Development
- Authentication & Authorization
- LangChain Framework
- Retrieval-Augmented Generation (RAG)
- Vector Databases (Pinecone)
- Prompt Engineering
- Large Language Models (LLMs)
- REST APIs
- Database Design
- Frontend Development
- Git & GitHub

---

# 👩‍💻 Author

**Gauri Gangwar**

B.Tech Computer Science Engineering

AI & Machine Learning Enthusiast

GitHub:
https://github.com/ggaurigangwar



---

# 📄 License

This project is licensed under the MIT License.

---

## ⭐ If you found this project helpful, consider giving it a star on GitHub!