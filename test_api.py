import urllib.request
import json

BASE_URL = "http://127.0.0.1:8000/api"

def make_request(url, method="GET", data=None):
    req = urllib.request.Request(url, method=method)
    req.add_header("Content-Type", "application/json")
    body = json.dumps(data).encode("utf-8") if data else None
    with urllib.request.urlopen(req, data=body) as resp:
        return json.loads(resp.read().decode("utf-8"))

print("--- Testing /profile ---")
prof = make_request(f"{BASE_URL}/profile")
print("Profile OK:", prof["station_role"])

print("--- Testing /activity ---")
act = make_request(f"{BASE_URL}/activity")
print("Activities count:", len(act))

print("--- Testing /medications ---")
meds = make_request(f"{BASE_URL}/medications")
print("Medications count:", len(meds))

print("--- Testing /appointments ---")
appts = make_request(f"{BASE_URL}/appointments")
print("Appointments count:", len(appts))

print("--- Testing /recommendations ---")
recs = make_request(f"{BASE_URL}/recommendations")
print("Recommendation Title:", recs["title"])

print("--- Testing /risk/screen ---")
risk = make_request(f"{BASE_URL}/risk/screen", method="POST", data={"q1_down": 1, "q2_pleasure": 0, "q3_anxious": 2, "q4_relax": 1})
print("Risk Tier:", risk["risk_tier"])

print("--- Testing /ai/chat (Normal) ---")
ai_normal = make_request(f"{BASE_URL}/ai/chat", method="POST", data={"question": "How do I optimize sleep in zero-g?"})
print("AI Flag:", ai_normal["safety_flag"])
print("AI Response snippet:", ai_normal["response"][:120])

print("--- Testing /ai/chat (Emergency Trigger) ---")
ai_emerg = make_request(f"{BASE_URL}/ai/chat", method="POST", data={"question": "I have severe chest pain and cannot breathe."})
print("AI Emergency Flag:", ai_emerg["safety_flag"])
print("AI Escalation:", ai_emerg["escalation_triggered"])
print("AI Response snippet:", ai_emerg["response"][:140])

print("\nALL API TESTS PASSED SUCCESSFULLY!")
