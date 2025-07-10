 Conversational AI Calendar Assistant

A fully functional AI-powered appointment booking assistant built with FastAPI, LangChain (Groq LLaMA3), and Google Calendar API, with a Streamlit chat‑style frontend. Users can ask natural language queries ("When am I free?", "Book 3 PM", "Cancel last booking") to check availability, create, and delete events in Google Calendar.

Live app: https://frontend-ai-assistance-jquob5idjkzsdqmb43enom.streamlit.app/
---

# Features

- **Natural‑language scheduling**  
  Suggests your next 3 free slots and lets you book by typing the time.
- **Two‑step confirmation**  
  “Book 4:30 PM” → “Yes” to finalize.
- **Event deletion**  
  “cancel” or “delete” removes the last booked event.
- **Stateful conversation**  
  Keeps track of suggested slots and booking state per chat session.
- **Secure credentials**  
  Uses `.env` for secret keys and service‑account JSON.

---

# Repository Structure

conversational_AI/
├── backend/
│ ├── agent.py # LangChain agent & tool definitions
│ ├── calendar_utils.py # Google Calendar API wrappers
│ ├── config.py # Loads .env variables
│ ├── credentials.json # Google service account (local only)
│ └── main.py # FastAPI app entrypoint
├── frontend/
│ └── app.py # Streamlit chat UI
├── .env.example # Sample environment variables
├── README.md # This file
└── requirements.txt # Python deps


---

#  Local Setup

1. **Clone the repo**  
   ``bash
   git clone https://github.com/yourusername/conversational_AI.git
   cd conversational_AI
Create & activate a virtual environment


python3 -m venv .venv
source .venv/bin/activate    # macOS/Linux
.\.venv\Scripts\activate     # Windows
Install dependencies


pip install -r requirements.txt
Configure environment

Copy .env.example → .env

Fill in your keys:


GROQ_API_KEY=your_groq_api_key
GOOGLE_CALENDAR_ID=your_calendar_id
GOOGLE_CREDENTIALS_PATH=backend/credentials.json
BACKEND_URL=http://localhost:8000
Place your service account JSON
Download from Google Cloud Console and save as backend/credentials.json.

Running Locally
Start the backend


uvicorn backend.main:app --reload
Start the frontend


streamlit run frontend/app.py
Interact
Open the Streamlit URL (usually http://localhost:8501) and chat:

“When am I free?”

“Book 3 PM”

“Yes”

“cancel”

 Deployment
Backend (Railway / Render / Fly.io)
Start command:


uvicorn backend.main:app --host 0.0.0.0 --port $PORT
Env vars: set GROQ_API_KEY, GOOGLE_CALENDAR_ID, GOOGLE_CREDENTIALS_PATH

Include credentials.json in backend/ (or use Base64 secret and decode)

Frontend (Streamlit Cloud)
Main file: frontend/app.py

Secrets: add BACKEND_URL=https://<your-backend-url>

 Environment Variables
Key	Purpose
GROQ_API_KEY	Groq LLaMA3 API key
GOOGLE_CALENDAR_ID	Calendar to read/write (e.g., primary)
GOOGLE_CREDENTIALS_PATH	Path to service account JSON (local)
BACKEND_URL	Streamlit → FastAPI base URL

 Tech Stack
Python 3.12

FastAPI + Uvicorn (backend)

LangChain (Groq LLaMA3) for agentic conversation

Google Calendar API (event CRUD & availability)

Streamlit (frontend chat UI)

python-dotenv for config

 Usage
Check availability:
“When am I free?”

Book a slot:
“Book 4:30 PM” → “Yes”

Cancel last booking:
“cancel” or “delete”

 License & Credits
MIT License © 2025 Pranav Baitule
Feel free to adapt and build upon this work.

 Contact
Pranav Baitule — GitHub | Email
