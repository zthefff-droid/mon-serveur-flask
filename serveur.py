import socket
import requests
import subprocess
import pyperclip
import logging
from datetime import datetime

# ═══════════════════════════════════════════════
# CHANGE CETTE LIGNE AVEC TON URL RENDER
# ═══════════════════════════════════════════════
RENDER_URL = "https://mon-serveur-flask-hmy4.onrender.com"
# ═══════════════════════════════════════════════

logging.basicConfig(
    filename="ip_log.txt",
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return socket.gethostbyname(socket.gethostname())

def get_public_ip():
    try:
        r = requests.get("https://api.ipify.org?format=json", timeout=10)
        if r.status_code == 200:
            return r.json()["ip"]
    except Exception:
        pass
    return None

def get_mac_address():
    try:
        output = subprocess.check_output(
            ["getmac", "/v", "/fo", "csv"],
            stderr=subprocess.DEVNULL
        ).decode()
        lines = output.strip().split("\n")
        if len(lines) > 1:
            return lines[1].split(",")[1].strip().strip('"')
    except Exception:
        pass
    return "N/A"

def send_ip():
    local_ip = get_local_ip()
    public_ip = get_public_ip()
    hostname = socket.gethostname()
    mac = get_mac_address()
    timestamp = datetime.now().isoformat()

    data = {
        "local_ip": local_ip,
        "public_ip": public_ip,
        "hostname": hostname,
        "mac_address": mac,
        "timestamp": timestamp
    }

    print(f"\n[ENVOI] {RENDER_URL}")
    print(f"[DONNÉES] {data}")

    try:
        response = requests.post(
            RENDER_URL,
            json=data,
            timeout=15,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )
        print(f"[RÉPONSE] {response.status_code} → {response.text}")

        if response.status_code == 200:
            print("[OK] Envoyé !")
            logging.info(f"Succès: {data}")
        else:
            print(f"[FAIL] Code: {response.status_code}")
            logging.error(f"Erreur: {response.text}")

    except Exception as e:
        print(f"[ERREUR] {e}")
        logging.error(str(e))

    # Copie dans le presse-papiers
    try:
        pyperclip.copy(local_ip)
        print(f"[CLIPBOARD] {local_ip}")
    except Exception:
        pass

    return data

if __name__ == "__main__":
    send_ip()
