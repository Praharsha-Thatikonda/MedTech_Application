class TriageService:
    def __init__(self):
        # Basic keyword-to-specialty mapping
        self.keywords = {
            "heart": "Cardiologist",
            "chest pain": "Cardiologist",
            "skin": "Dermatologist",
            "rash": "Dermatologist",
            "acne": "Dermatologist",
            "headache": "Neurologist",
            "dizzy": "Neurologist",
            "kid": "Pediatrician",
            "child": "Pediatrician",
            "baby": "Pediatrician",
            "fever": "General",
            "flu": "General"
        }

    def analyze_symptoms(self, text):
        """
        Returns a recommended specialty based on text.
        """
        text = text.lower()
        for key, specialty in self.keywords.items():
            if key in text:
                return specialty
        return "General"

    def is_emergency(self, text):
        """
        Detects if input sounds like a critical emergency.
        """
        emergencies = ["heart attack", "stroke", "bleeding", "unconscious", "harrt pain", "dying", "emergency"]
        text = text.lower()
        return any(e in text for e in emergencies)

triage_service = TriageService()
