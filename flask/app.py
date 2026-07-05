from flask import Flask, render_template, request, jsonify, g
from models import SessionLocal, engine, Base, User, Doctor, Hospital, ChatSession, ChatMessage
import random
import sys
import os

# Add parent dir to path for shared LLM service
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from llm_service import llm_service
try:
    from databases.sql_manager import sql_manager
except ImportError:
    # If standard import fails, try path hack again (though already done above)
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'databases'))
    from sql_manager import sql_manager

# Initialize Database (User data mainly now)
Base.metadata.create_all(bind=engine)

app = Flask(__name__)

# --- DB HELPERS ---
def get_db():
    if 'db' not in g:
        g.db = SessionLocal()
    return g.db

@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# --- SEED DATA ---
def seed_data():
    db = SessionLocal()
    try:
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
    finally:
        db.close()

# Run seed
seed_data()

# --- ROUTES ---

@app.route('/')
def home():
    db = get_db()
    user = db.query(User).first()
    doctors = db.query(Doctor).limit(3).all()
    hospitals = db.query(Hospital).limit(3).all()
    sessions = db.query(ChatSession).order_by(ChatSession.created_at.desc()).all()
    
    # current_session = sessions[0] if sessions else None
    # CHANGE: Do not auto-select latest session. Start fresh unless requested.
    session_id_param = request.args.get("session_id")
    current_session = None
    if session_id_param:
         # Find session by ID - sessions is a list, iterating is fast enough for small N
         current_session = next((s for s in sessions if str(s.id) == session_id_param), None)

    messages = []
    if current_session:
        messages = db.query(ChatMessage).filter(ChatMessage.session_id == current_session.id).all()

    return render_template("index.html", 
        user=user,
        doctors=doctors,
        hospitals=hospitals,
        sessions=sessions,
        current_session=current_session,
        messages=messages
    )

@app.route('/api/chat', methods=['POST'])
def chat():
    db = get_db()
    data = request.json
    text = data.get('text', '')
    session_id = data.get('session_id', 1)
    
    # Save User Msg
    user_msg = ChatMessage(session_id=session_id, sender="user", content=text)
    db.add(user_msg)
    
    # Logic
    # Logic - LLM Integration
    try:
        model_key = data.get('model', 'gemma-it')
        
        # Build Context (From Central Main DB for Doctors/Hospitals)
        # We use sql_manager directly which returns list of dicts - ideal for llm_service
        try:
            doctors_list = sql_manager.get_all_doctors()
            hospitals_list = sql_manager.get_all_hospitals()
        except:
            doctors_list = []
            hospitals_list = []
            
        context = {
            'doctors': doctors_list,
            'hospitals': hospitals_list,
            'user_coords': data.get('coords') # Get from Frontend JSON
        }
        
        reply_content = llm_service.generate_response(text, model_key=model_key, context=context)
    except Exception as e:
        print(f"LLM Error: {e}")
        reply_content = "I apologize, but I'm having trouble thinking right now. Please check my connection."
        
    # Save AI Msg
    ai_msg = ChatMessage(session_id=session_id, sender="ai", content=reply_content)
    db.add(ai_msg)
    db.commit()
    
    return jsonify({"reply": reply_content})

class SimpleObj:
    def __init__(self, dictionary):
        for k, v in dictionary.items():
            setattr(self, k, v)

@app.route('/doctors')
def doctors():
    # Use Central Main DB
    raw_docs = sql_manager.get_all_doctors()
    doctors = [SimpleObj(d) for d in raw_docs]
    return render_template('doctors.html', doctors=doctors)

@app.route('/hospitals')
def hospitals():
    # Use Central Main DB
    raw_hosp = sql_manager.get_all_hospitals()
    hospitals = [SimpleObj(h) for h in raw_hosp]
    return render_template('hospitals.html', hospitals=hospitals)

@app.route('/transportation')
def transportation():
    return render_template('transportation.html')
    
@app.route('/ailab')
def ailab():
    return render_template('ailab.html')

@app.route('/map')
def map_view():
    return render_template('map.html')

@app.route('/profile')
def profile():
    db = get_db()
    user = db.query(User).first()
    return render_template('profile.html', user=user)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
