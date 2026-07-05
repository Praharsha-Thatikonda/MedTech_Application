def get_mock_data():
    # Real-world locations (approx coordinates for India)
    doctors = [
        {"id": 1, "name": "Dr. Rajesh Kumar", "specialty": "Cardiologist", "location": "Mumbai, Maharashtra", "coords": (19.0760, 72.8777), "status": "Available", "rating": 4.9},
        {"id": 2, "name": "Dr. Anita Sharma", "specialty": "Neurologist", "location": "Delhi, NCR", "coords": (28.7041, 77.1025), "status": "Busy", "rating": 4.8},
        {"id": 3, "name": "Dr. Priya Reddy", "specialty": "Dermatologist", "location": "Bangalore, Karnataka", "coords": (12.9716, 77.5946), "status": "Available", "rating": 4.7},
        {"id": 4, "name": "Dr. Vikram Singh", "specialty": "Pediatrician", "location": "Hyderabad, Telangana", "coords": (17.3850, 78.4867), "status": "Offline", "rating": 4.6},
        {"id": 5, "name": "Dr. Meera Iyer", "specialty": "General", "location": "Chennai, Tamil Nadu", "coords": (13.0827, 80.2707), "status": "Available", "rating": 4.8},
        {"id": 6, "name": "Dr. Amit Patel", "specialty": "Orthopedic", "location": "Ahmedabad, Gujarat", "coords": (23.0225, 72.5714), "status": "Available", "rating": 4.5},
    ]
    
    hospitals = [
        {"id": 1, "name": "AIIMS Delhi", "location": "New Delhi", "coords": (28.5672, 77.2100), "open_hours": "24/7", "type": "Government/Research"},
        {"id": 2, "name": "Apollo Hospital", "location": "Chennai", "coords": (13.0630, 80.2550), "open_hours": "24/7", "type": "Multi-Specialty"},
        {"id": 3, "name": "Fortis Hospital", "location": "Mumbai", "coords": (19.1630, 72.9430), "open_hours": "24/7", "type": "Private"},
        {"id": 4, "name": "Manipal Hospital", "location": "Bangalore", "coords": (12.9592, 77.6475), "open_hours": "24/7", "type": "Private"},
        {"id": 5, "name": "Tata Memorial Hospital", "location": "Mumbai", "coords": (19.0060, 72.8410), "open_hours": "24/7", "type": "Cancer Care"},
    ]
    return {"doctors": doctors, "hospitals": hospitals}
