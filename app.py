from flask import Response, stream_with_context
from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    flash,
)
from flask_login import login_user, logout_user, login_required, current_user
from dotenv import load_dotenv
from src.chat_manager import ChatManager
from datetime import datetime
import json


from extensions import db, bcrypt, login_manager
from models import User, UserProfile, Consultation 


import os

from langchain_pinecone import PineconeVectorStore
from langchain_ollama import ChatOllama
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

from src.helper import download_hugging_face_embeddings
from src.prompt import *

app = Flask(__name__)

# Secret key for session management
app.config["SECRET_KEY"] = "your_super_secret_key"

# SQLite Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)

load_dotenv()

embedding = download_hugging_face_embeddings()


index_name = "medical-chatbot"

docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embedding
)


retriever = docsearch.as_retriever(
    search_type="similarity",
    search_kwargs={"k":3}
)


llm = ChatOllama(
    model="llama3",
    temperature=0
)


question_answer_chain = create_stuff_documents_chain(
    llm,
    prompt
)

rag_chain = create_retrieval_chain(
    retriever,
    question_answer_chain
)

chat_manager = ChatManager(
    retriever=retriever,
    rag_chain=rag_chain,
    llm=llm
)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def home():

    auth = request.args.get("auth", "")

    return render_template(
        "dashboard.html",
        auth=auth,
        user=current_user
    )


@app.route("/start-consultation")
def start_consultation():

    if current_user.is_authenticated:
        return redirect(url_for("chat"))

    return redirect(url_for("home"))


@app.route("/signup", methods=["POST"])
def signup():

    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")

    # Check empty fields
    if not name or not email or not password or not confirm_password:

        flash("Please fill in all fields.", "danger")

        return redirect(url_for("home"))

    # Password match
    if password != confirm_password:

        flash("Passwords do not match.", "danger")

        return redirect(url_for("home"))

    # Existing email
    existing_user = User.query.filter_by(email=email).first()

    if existing_user:

        flash("Email already registered.", "warning")

        return redirect(url_for("home", auth="signup"))

    # Hash password
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    # Create User
    user = User(
        name=name,
        email=email,
        password=hashed_password
    )

    db.session.add(user)
    db.session.commit()

    # Login Automatically
    login_user(user, remember=True)

    flash("Welcome to VitaCare!", "success")

    return redirect(url_for("chat"))




@app.route("/login", methods=["POST"])
def login():

    # Already logged in
    if current_user.is_authenticated:
        return redirect(url_for("chat"))

    email = request.form.get("email")
    password = request.form.get("password")

    # Empty fields
    if not email or not password:

        flash("Please fill in all fields.", "danger")

        return redirect(url_for("home", auth="login"))

    # Find user
    user = User.query.filter_by(email=email).first()

    # Verify password
    if user and bcrypt.check_password_hash(user.password, password):

        login_user(user, remember=True)

        flash(f"Welcome back, {user.name}!", "success")

        return redirect(url_for("chat"))

    flash("Invalid email or password.", "danger")

    return redirect(url_for("home"))


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)



@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():

    profile = current_user.profile

    if request.method == "POST":

        if profile is None:
            profile = UserProfile(user=current_user)

        dob = request.form.get("dob")

        profile.dob = datetime.strptime(dob, "%Y-%m-%d").date() if dob else None
        profile.gender = request.form.get("gender")
        profile.height = request.form.get("height") or None
        profile.weight = request.form.get("weight") or None
        profile.blood_group = request.form.get("blood_group")
        profile.existing_disease = request.form.get("existing_disease")
        profile.allergies = request.form.get("allergies")
        profile.current_medications = request.form.get("current_medications")

        db.session.add(profile)
        db.session.commit()

        flash("Profile updated successfully!", "success")

        return redirect(url_for("dashboard"))

    return render_template("profile.html", profile=profile)


@app.route("/logout")
@login_required
def logout():

    logout_user()

    flash("Logged out successfully!", "success")

    return redirect(url_for("home"))



@app.route("/chat")
@login_required
def chat():

    return render_template(
        "chat.html",
        user=current_user,
        title="VitaCare Chat"
    )


@app.route("/stream", methods=["POST"])
@login_required
def stream():

    data = request.get_json()
    question = data["message"]
    print("Received from frontend:", question)
    clean_question = question.strip().lower()
    print("Clean question:", clean_question)

    print("Original Question:", question)
    print("Clean Question:", clean_question)

    simple_responses = {
        "hi": "Hello! 👋 How can I help you with your health today?",
        "hello": "Hello! 👋 How can I assist you today?",
        "hey": "Hi! 😊 What health concern can I help you with?",
        "good morning": "Good morning! ☀️ How can I help you today?",
        "good afternoon": "Good afternoon! 😊 How can I assist you today?",
        "good evening": "Good evening! 🌙 How can I help you today?",
        "thanks": "You're welcome! 😊 Take care and stay healthy.",
        "thank you": "You're welcome! 😊 Wishing you good health.",
        "bye": "Goodbye! 👋 Take care and stay healthy.",
        "goodbye": "Goodbye! 👋 Wishing you good health.",
        "good night": "Good night! 🌙 Take care."
    }

    # Handle greetings
    if clean_question in simple_responses:

        def generate():
            yield simple_responses[clean_question]

        return Response(
            stream_with_context(generate()),
            mimetype="text/plain"
        )

    # Handle vague or incomplete queries
    vague_queries = [
        "i have a query",
        "i have question",
        "i have a question",
        "query",
        "question",
        "help",
        "can you help me",
        "need help",
        "can i ask something"
    ]

    if clean_question in vague_queries:

        def generate():
            yield (
                "I'd be happy to help! 😊\n\n"
                "Please describe your symptoms or ask your health-related question.\n\n"
            )

        return Response(
            stream_with_context(generate()),
            mimetype="text/plain"
        )

    # Handle empty message
    if not clean_question:

        def generate():
            yield "Please enter your health-related question."

        return Response(
            stream_with_context(generate()),
            mimetype="text/plain"
        )

    # Medical queries
    profile = current_user.profile

    profile_context = ""

    if profile:
        profile_context = f"""
Patient Information:

Gender: {profile.gender}
Blood Group: {profile.blood_group}
Height: {profile.height} cm
Weight: {profile.weight} kg
Existing Diseases: {profile.existing_disease}
Allergies: {profile.allergies}
Current Medications: {profile.current_medications}
"""

    final_question = f"""
{profile_context}

Patient Question:

{question}
"""

    def generate():
        answer = chat_manager.handle_query(final_question)
        yield answer

    return Response(
        stream_with_context(generate()),
        mimetype="text/plain"
    )



@app.route("/save-consultation", methods=["POST"])
@login_required
def save_consultation():

    data = request.get_json()

    conversation = data.get("conversation")

    print("\n========== Conversation Received ==========")
    for msg in conversation:
        print(msg["role"], ":", msg["message"][:80])
    print("==========================================\n")

    if not conversation:
        return jsonify({
            "success": False,
            "message": "Nothing to save."
        }), 400

    title = "Medical Consultation"

    ignore_titles = [
        "hi", "hello", "hey",
        "how are you",
        "who are you",
        "what is your name",
        "thanks",
        "thank you",
        "bye"
    ]

    for msg in conversation:

        if msg["role"] != "user":
            continue

        question = msg["message"].strip().lower()

        if any(ignore in question for ignore in ignore_titles):
            continue

        title = msg["message"][:60]
        break

    consultation = Consultation(
        user_id=current_user.id,
        title=title,
        conversation=json.dumps(conversation)
    )

    db.session.add(consultation)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Consultation saved successfully."
    })

@app.route("/history")
@login_required
def history():

    consultations = Consultation.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Consultation.created_at.desc()
    ).all()

    return render_template(
        "history.html",
        consultations=consultations,
        json=json
    )

print("\nRegistered Routes:")
print(app.url_map)
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True, use_reloader=False)