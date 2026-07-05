from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models
from models import SessionLocal, engine, Doctor, Hospital, ChatSession, ChatMessage, User
import random
import os
import sys

# Add parent dir
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from llm_service import llm_service

try:
    from databases.sql_manager import sql_manager
except ImportError:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'databases'))
    from sql_manager import sql_manager

# Initialize Database (User data mainly)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- SEED DATA ---
def seed_data(db: Session):
    # Seed User
    if not db.query(User).first():
        user = User(
            name="Alex Morgan",
            email="alex@medtech.com",
            phone="+1 (555) 019-2834",
            age=34,
            blood_type="O+",
            conditions="Mild Asthma",
            avatar_url="https://ui-avatars.com/api/?name=Alex+Morgan&background=ebf8ff&color=2563eb&size=128"
        )
        db.add(user)

    # Seed Doctors
    if not db.query(Doctor).first():
        doctors = [
            Doctor(name="Dr. Sarah Smith", specialty="Cardiologist", status="Available", phone="+1 555-0123", location="City General Hospital", experience="15 Years", rating="4.9", reviews=128, avatar_url="https://ui-avatars.com/api/?name=Sarah+Smith&background=e0e7ff&color=4f46e5&size=128"),
            Doctor(name="Dr. James Wilson", specialty="Neurologist", status="Offline", phone="+1 555-0124", location="Neuropath Clinic", experience="8 Years", rating="4.7", reviews=84, avatar_url="https://ui-avatars.com/api/?name=James+Wilson&background=f0fdf4&color=16a34a&size=128"),
            Doctor(name="Dr. Emily Chen", specialty="Pediatrician", status="Available", phone="+1 555-0125", location="Family Care Center", experience="12 Years", rating="4.8", reviews=210, avatar_url="https://ui-avatars.com/api/?name=Emily+Chen&background=fff7ed&color=c2410c&size=128")
        ]
        db.add_all(doctors)
        
    # Seed Hospitals
    if not db.query(Hospital).first():
        hospitals = [
            Hospital(name="City General Hospital", location="123 Health Ave, Metro City", phone="+1 555-9000", status_color="green", open_hours="24/7", tags="Trauma Center,ICU,Pediatrics"),
            Hospital(name="St. Mary's Clinic", location="45 West Street, Downtown", phone="+1 555-9001", status_color="orange", open_hours="Closes 8 PM", tags="General Medicine,Pharmacy"),
            Hospital(name="Westside Urgent Care", location="88 Broadway", phone="+1 555-9002", status_color="green", open_hours="24/7", tags="Emergency,Lab Services")
        ]
        db.add_all(hospitals)
        
        # Create initial session
        if not db.query(ChatSession).first():
            session = ChatSession(title="New Session")
            db.add(session)
        
        db.commit()

# Run seed on startup
@app.on_event("startup")
def on_startup():
    with SessionLocal() as db:
        seed_data(db)

# --- Pydantic Models for API ---
class MessageRequest(BaseModel):
    text: str
    session_id: int = 1
    model: str = 'gemma-it'
    coords: list = None
    image_data: str = None # Base64 string

# --- ROUTES ---

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: Session = Depends(get_db)):
    user = db.query(User).first()
    doctors = db.query(Doctor).limit(3).all()
    hospitals = db.query(Hospital).limit(3).all()
    sessions = db.query(ChatSession).order_by(ChatSession.created_at.desc()).all()
    
    # current_session = sessions[0] if sessions else None
    # CHANGE: Do not auto-select latest session. Start fresh unless requested.
    session_id_param = request.query_params.get("session_id")
    current_session = None
    if session_id_param:
         # Find session by ID
         current_session = next((s for s in sessions if str(s.id) == session_id_param), None)

    messages = []
    if current_session:
        messages = db.query(ChatMessage).filter(ChatMessage.session_id == current_session.id).all()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "user": user,
        "doctors": doctors,
        "hospitals": hospitals,
        "sessions": sessions,
        "current_session": current_session,
        "messages": messages
    })

@app.post("/api/chat")
async def chat_endpoint(request: MessageRequest, db: Session = Depends(get_db)):
    # Store User Message
    content_to_store = request.text
    if request.image_data:
        content_to_store += " [Image Attachment]"
        
    user_msg = ChatMessage(session_id=request.session_id, sender="user", content=content_to_store)
    db.add(user_msg)
    
    # LLM Integration
    import sys
    import os
    if os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) not in sys.path:
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        
    try:
        from llm_service import llm_service
        
        # Build Context (Central DB)
        try:
            doctors_list = sql_manager.get_all_doctors()
            hospitals_list = sql_manager.get_all_hospitals()
        except:
            doctors_list = []
            hospitals_list = []

        context = {
            'doctors': doctors_list,
            'hospitals': hospitals_list,
            'user_coords': request.coords
        }
        
        # Modify prompt if image included
        text_to_llm = request.text
        if request.image_data:
            text_to_llm += "\n[System: User uploaded an image. Acknowledge receipt. Since Vision is offline, ask the user to describe the image features for analysis.]"
        
        reply_content = llm_service.generate_response(text_to_llm, model_key=request.model, context=context)
    except Exception as e:
        print(f"LLM Error: {e}")
        reply_content = "System Error: Unable to reach AI brain."
    
    ai_msg = ChatMessage(session_id=request.session_id, sender="ai", content=reply_content)
    db.add(ai_msg)
    db.commit()
    return {"reply": reply_content}

class SimpleObj:
    def __init__(self, dictionary):
        for k, v in dictionary.items():
            setattr(self, k, v)

@app.route('/doctors') # Note: FastAPI uses @app.get, correcting this below
@app.get("/doctors", response_class=HTMLResponse)
async def doctors_page(request: Request):
    # Use Central Main DB
    raw_docs = sql_manager.get_all_doctors()
    doctors = [SimpleObj(d) for d in raw_docs]
    return templates.TemplateResponse("doctors.html", {"request": request, "doctors": doctors})

@app.get("/hospitals", response_class=HTMLResponse)
async def hospitals_page(request: Request):
    # Use Central Main DB
    raw_hosp = sql_manager.get_all_hospitals()
    hospitals = [SimpleObj(h) for h in raw_hosp]
    return templates.TemplateResponse("hospitals.html", {"request": request, "hospitals": hospitals})

@app.get("/profile", response_class=HTMLResponse)
async def profile_page(request: Request, db: Session = Depends(get_db)):
    user = db.query(User).first()
    return templates.TemplateResponse("profile.html", {"request": request, "user": user})

@app.get("/ailab", response_class=HTMLResponse)
async def ailab_page(request: Request):
    return templates.TemplateResponse("ailab.html", {"request": request})

@app.get("/map", response_class=HTMLResponse)
async def map_page(request: Request):
    return templates.TemplateResponse("map.html", {"request": request})

@app.get("/transportation", response_class=HTMLResponse)
async def transportation_page(request: Request):
    return templates.TemplateResponse("transportation.html", {"request": request})

# Simulated Analysis Endpoint
@app.post("/api/analyze")
async def analyze_report():
    import time
    time.sleep(1) # Simulate processing
    return {"result": "Analysis Complete: No significant abnormalities detected. Vitamin D levels are slightly low."}
