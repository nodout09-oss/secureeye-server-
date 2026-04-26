
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.json
        api_key = data.get("api_key", "")
        description = data.get("description", "")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-pro")
        prompt = f"""
        You are a security AI analyst.
        Analyze this incident: {description}
        Respond in JSON:
        {{
            "incident_type": "type",
            "threat_level": "1-10",
            "is_theft": true or false,
            "recommended_action": "action",
            "alert_message": "message"
        }}
        """
        response = model.generate_content(prompt)
        return jsonify({"success": True, "analysis": response.text})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/status", methods=["GET"])
def status():
    return jsonify({
        "status": "SecureEye AI Server Running",
        "time": datetime.now().isoformat()
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
