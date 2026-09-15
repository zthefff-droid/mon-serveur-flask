from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/receive", methods=["POST"])
def receive():
    data = request.get_json()

    print("Donnée reçue :", data)

    with open("ips_recues.txt", "a", encoding="utf-8") as f:
        f.write(str(data) + "\n")

    return jsonify({"status": "ok"})