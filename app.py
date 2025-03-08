from fastapi import FastAPI, Request
import requests
from biogpt_model import analyze_drug_interaction
from firebase_utils import save_patient_data, get_patient_history

app = FastAPI()

# WhatsApp API Configuration (Replace with your details)
WHATSAPP_API_URL = "https://graph.facebook.com/v18.0/YOUR_PHONE_NUMBER_ID/messages"
WHATSAPP_ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"

@app.post("/webhook")
async def receive_message(request: Request):
    """
    Handles incoming WhatsApp messages, analyzes drug interactions,
    stores patient history, and responds with AI-generated insights.
    """
    data = await request.json()

    try:
        message = data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
        sender = data['entry'][0]['changes'][0]['value']['messages'][0]['from']

        # Extract patient ID and prescription from message
        parts = message.split("\n")
        patient_id = parts[0].replace("Patient ID: ", "").strip()
        prescription = parts[1].replace("Prescription: ", "").strip()

        # Get AI-generated analysis from BioGPT
        analysis = analyze_drug_interaction(prescription)

        # Save data to Firebase Firestore
        save_patient_data(patient_id, prescription, analysis)

        # Fetch patient's prescription history
        history = get_patient_history(patient_id)
        history_text = f"\nPrevious Prescriptions: {history['prescription']}" if history else ""

        # Send AI-generated response back to WhatsApp
        response_text = f"**Drug Interaction Analysis:**\n{analysis}\n{history_text}"
        requests.post(WHATSAPP_API_URL, json={
            "messaging_product": "whatsapp",
            "to": sender,
            "text": {"body": response_text}
        }, headers={"Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}"})

        return {"status": "ok"}

    except Exception as e:
        print(f"Error: {e}")
        return {"status": "error"}
