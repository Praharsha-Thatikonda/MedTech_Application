import os
import sys
import multiprocessing

# --- 1. Import Dependencies & Backend Services ---
try:
    from llama_cpp import Llama
except ImportError:
    print("Error: llama-cpp-python is not installed. Please install it (pip install llama-cpp-python).")
    Llama = None

# Attempt to import custom backend modules
try:
    from backend.search_engine import search_engine
    from backend.geo_service import geo_service
    from backend.triage_service import triage_service
    
    # New Database Modules
    from databases.vector_store import vector_store
    from databases.graph_store import graph_store
    from databases.cache_store import cache_store
    from databases.sql_manager import sql_manager
except ImportError:
    # Handle relative pathing for sub-frameworks (flask/django/fastapi runners)
    try:
        sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
        sys.path.append(os.path.join(os.path.dirname(__file__), 'databases'))
        
        from search_engine import search_engine
        from geo_service import geo_service
        from triage_service import triage_service
        
        # New DBs
        from vector_store import vector_store
        from graph_store import graph_store
        from cache_store import cache_store
        from sql_manager import sql_manager
        
    except Exception as e:
        print(f"Warning: Backend/Database modules could not be loaded: {e}")
        search_engine = None
        geo_service = None
        triage_service = None
        vector_store = None
        graph_store = None
        cache_store = None
        sql_manager = None

# --- 2. LLM Service Class ---
class LLMService:
    _instance = None
    _model = None
    _current_model_path = None

    # Available Models Map
    MODELS = {
        "gemma-it": os.path.join("models", "gemma-3-gguf-gemma-3-4b-it-qat-q4_0-v3", "gemma-3-4b-it-q4_0.gguf"),
        "gemma-pt": os.path.join("models", "gemma-3-gguf-gemma-3-4b-pt-qat-q4_0-v1", "gemma-3-4b-pt-q4_0.gguf")
    }

    def __init__(self):
        # Initial load (default to IT)
        self.load_model("gemma-it")

    def load_model(self, model_key):
        if model_key not in self.MODELS:
            print(f"Warning: Model {model_key} not found. Defaulting to gemma-it.")
            model_key = "gemma-it"
            
        target_rel_path = self.MODELS[model_key]
        
        # Resolve absolute path (Robust finder)
        possible_paths = [
            os.path.join(os.getcwd(), target_rel_path),
            os.path.join(os.path.dirname(os.getcwd()), target_rel_path),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), target_rel_path),
            os.path.join("C:\\Users\\praha\\Documents\\a_Medical_app\\frentend\\f_two", target_rel_path)
        ]
        
        final_path = None
        for p in possible_paths:
            if os.path.exists(p):
                final_path = p
                break
        
        if not final_path:
            print(f"Error: Could not find model file for {model_key}")
            return

        # If already loaded, skip
        if LLMService._current_model_path == final_path and LLMService._model is not None:
            return

        print(f"Loading LLM ({model_key}) from: {final_path}...")
        
        # --- GPU / CPU Hardware Config ---
        try:
            # Unload previous to free VRAM
            if LLMService._model:
                del LLMService._model
                LLMService._model = None
            
            cpu_count = multiprocessing.cpu_count()
            
            # ATTEMPT 1: Aggressive GPU Load (Ollama Style)
            try:
                print(f"1. Attempting GPU load (n_gpu_layers=-1) on {final_path}...")
                print("   - This will offload ALL layers to the NVIDIA GPU if CUDA is available.")
                print("   - If CUDA is not found, it will gracefully fallback to CPU.")
                
                LLMService._model = Llama(
                    model_path=final_path,
                    n_gpu_layers=-1,      # FORCE GPU (Offload all layers)
                    main_gpu=0,           # Use Primary GPU
                    n_ctx=4096,
                    n_batch=2048,         
                    n_threads=max(1, cpu_count - 1),
                    use_mmap=True,        
                    use_mlock=False,
                    verbose=True
                )
                print(">>> SUCCESS: Model Loaded. (Check console for 'ggml_cuda_init: found X CUDA devices' to verify GPU usage)")
            except Exception as gpu_err:
                print(f"GPU Load Failed: {gpu_err}. Falling back to standard CPU mode...")
                
                # ATTEMPT 2: Safe CPU Load
                LLMService._model = Llama(
                    model_path=final_path,
                    n_gpu_layers=0,       # CPU Only
                    n_ctx=2048,           # Smaller context for safety
                    n_batch=512,
                    n_threads=max(1, cpu_count - 1),
                    verbose=True
                )
                print(">>> SUCCESS: Loaded on CPU.")
            
            LLMService._current_model_path = final_path
            
        except Exception as e:
            print(f"CRITICAL ERROR: Failed to load model: {e}")

    def generate_response(self, user_text, model_key="gemma-it", context=None):
        # Ensure correct model is loaded
        if not LLMService._model:
            self.load_model(model_key)
        
        if not LLMService._model:
            return "Error: AI Model could not be loaded. Please check the server console for paths."

        # RAG Logic (Retrieval Augmented Generation)
        rag_info = ""
        user_coords = context.get('user_coords') if context else None

        if context:
            # 1. TRIAGE ANALYSIS
            suggested_specialty = None
            is_emergency = False
            
            if triage_service:
                try:
                    is_emergency = triage_service.is_emergency(user_text)
                    suggested_specialty = triage_service.analyze_symptoms(user_text)
                except Exception as e:
                    print(f"[LLM] Triage Service Error: {e}")

            # 2. EMERGENCY CHECK
            if is_emergency:
                rag_info += "\n[!!! SYSTEM ALERT: EMERGENCY DETECTED !!!]\nRecommending immediate closest hospitals:\n"
                # Prioritize Hospitals
                candidates = context.get('hospitals', [])
                if geo_service and user_coords:
                    try:
                        candidates = geo_service.find_nearby(user_coords, candidates)
                    except Exception as e:
                        print(f"[LLM] Geo Service Error (Hospitals): {e}")
                
                for h in candidates[:3]:
                    name = h.get('name', 'Unknown')
                    loc = h.get('location', 'Unknown')
                    dist = f"({h.get('distance_km')} km away)" if h.get('distance_km') else ""
                    rag_info += f"- {name} {dist} - {loc}\n"
            
            else:
                # 3. DOCTOR SEARCH
                doc_candidates = context.get('doctors', [])
                
                # Filter by specialty if found (and not generic)
                if suggested_specialty and suggested_specialty != "General":
                    filtered = [d for d in doc_candidates if d.get('specialty') == suggested_specialty]
                    if filtered:
                        doc_candidates = filtered
                
                # Sort by distance
                if geo_service and user_coords:
                    try:
                        doc_candidates = geo_service.find_nearby(user_coords, doc_candidates)
                    except Exception as e:
                        print(f"[LLM] Geo Service Error (Doctors): {e}")
                
                # Add to prompt
                if doc_candidates:
                    rag_info += f"\n[RAG: Found Specialists for '{suggested_specialty or 'General'}']:\n"
                    for d in doc_candidates[:3]:
                        name = d.get('name')
                        spec = d.get('specialty')
                        loc = d.get('location')
                        dist = f"({d.get('distance_km')} km)" if d.get('distance_km') else ""
                        rag_info += f"- Dr. {name} ({spec}) {dist} at {loc}\n"

            # 4. KB/VECTOR SEARCH (Semantic Memory)
            if vector_store:
                try:
                    kb_results = vector_store.search(user_text)
                    if kb_results and kb_results['documents']:
                        rag_info += "\n[KNOWLEDGE BASE]:\n"
                        # Limit to 2 docs (flatten list if needed)
                        documents = kb_results['documents']
                        # Chroma sometimes returns list of lists
                        if documents and isinstance(documents[0], list):
                             documents = documents[0]
                        
                        for doc in documents[:2]:
                            rag_info += f"- {doc}\n"
                except Exception as e:
                    print(f"[LLM] Vector Store Error: {e}")

        # Gemma Prompt Format
        system_prompt = (
            "You are Dr. AI Assistant, a medical expert helping patients in India. "
            "Provide helpful, safe medical advice. "
            "If real-time data or emergency alerts are provided below, prioritize them instantly. "
            "Always be polite and professional."
        )
        
        # Truncate RAG info if too long (safety)
        if len(rag_info) > 2000:
            rag_info = rag_info[:2000] + "...(truncated)"

        if rag_info:
            full_prompt = f"<start_of_turn>user\n{system_prompt}\n\n[REAL-TIME DATA FOUND]:{rag_info}\n\nUser Question: {user_text}<end_of_turn>\n<start_of_turn>model\n"
        else:
            full_prompt = f"<start_of_turn>user\n{system_prompt}\n\n{user_text}<end_of_turn>\n<start_of_turn>model\n"
        
        try:
            output = LLMService._model(
                full_prompt,
                max_tokens=600,
                stop=["<end_of_turn>", "User:"],
                echo=False,
                temperature=0.7
            )
            return output['choices'][0]['text'].strip()
        except Exception as e:
            import traceback
            print(f"CRITICAL GENERATION ERROR: {e}")
            print(traceback.format_exc())
            return "I apologize, but I encountered an internal error while processing your request. Please try again."

# Singleton instance access
llm_service = LLMService()
