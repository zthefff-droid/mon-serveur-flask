from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)  # Autorise les requêtes depuis n'importe où

# Stockage en mémoire (ou utilise une base de données)
received_ips = []

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "online", "timestamp": datetime.now().isoformat()})

@app.route("/api/ip", methods=["POST"])
def receive_ip():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data"}), 400

        # Ajoute le timestamp serveur
        data["received_at"] = datetime.now().isoformat()
        received_ips.append(data)

        print(f"[RECEIVED] {data}")  # Visible dans les logs Render
        return jsonify({"status": "ok", "message": "IP received", "data": data}), 200

    except Exception as e:
        print(f"[ERROR] {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/ips", methods=["GET"])
def get_ips():
    """Pour vérifier toutes les IPs reçues."""
    return jsonify({"count": len(received_ips), "ips": received_ips}), 200

@app.route("/api/ip/<ip>", methods=["GET"])
def get_ip(ip):
    """Récupère une IP spécifique."""
    found = [i for i in received_ips if i.get("local_ip") == ip]
    return jsonify({"results": found}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
