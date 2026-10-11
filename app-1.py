import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

# المواقع اللي هنجرب نتصل بيها من السيرفر
TARGETS = {
    "gemini": "https://generativelanguage.googleapis.com",
    "google": "https://www.google.com",
}

# لو حطيت SUPABASE_URL في Environment هيتجرب كمان
if os.environ.get("SUPABASE_URL"):
    TARGETS["supabase"] = os.environ["SUPABASE_URL"].rstrip("/")


@app.route("/")
def home():
    return jsonify({"status": "ok", "message": "السيرفر شغال"})


@app.route("/check")
def check():
    results = {}
    for name, url in TARGETS.items():
        try:
            r = requests.get(url, timeout=8)
            # أي رد (حتى 403 أو 404) معناه إن الاتصال نجح
            results[name] = {"connected": True, "http_status": r.status_code}
        except Exception as e:
            results[name] = {"connected": False, "error": str(e)[:200]}
    return jsonify(results)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
