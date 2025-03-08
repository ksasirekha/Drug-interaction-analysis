import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase using the key file
cred = credentials.Certificate("firebase_key.json")  # Ensure this file is in the project directory
firebase_admin.initialize_app(cred)
db = firestore.client()

def save_patient_data(patient_id, prescription, analysis):
    """Store patient prescription & analysis in Firestore."""
    doc_ref = db.collection("patients").document(patient_id)
    doc_ref.set({
        "patient_id": patient_id,
        "prescription": prescription,
        "analysis": analysis
    })

def get_patient_history(patient_id):
    """Retrieve patient’s prescription history."""
    doc_ref = db.collection("patients").document(patient_id)
    doc = doc_ref.get()
    return doc.to_dict() if doc.exists else None

# Test Firestore connection
if __name__ == "__main__":
    test_id = "P12345"
    test_prescription = "Paracetamol + Ibuprofen"
    test_analysis = "Mild interaction. Avoid if patient has liver issues."

    save_patient_data(test_id, test_prescription, test_analysis)
    print("Saved test patient data!")

    history = get_patient_history(test_id)
    print("Retrieved history:", history)
