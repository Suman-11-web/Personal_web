import json
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__, static_folder="static")
app.secret_key = "super_secret_epic_key"
DATA_FILE = "data.json"

def load_data():
    default_data = {
        "about_text": "1. I have a strong interest in programming.\n2. I enjoy working with Python, HTML, CSS, and JavaScript.\n3. Currently learning and building projects step by step.",
        "insta_link": "https://instagram.com/__suman._.007",
        "focus_1_title": "Web Development",
        "focus_1_desc": "Interactive web apps",
        "focus_1_link": "#",
        "focus_2_title": "UI/Graphics Design",
        "focus_2_desc": "Clean & modern interfaces",
        "focus_2_link": "#",
        "projects": [
            {"name": "Novasocial", "desc": "A full-fledged social media application designed to connect users.", "link": "#"},
            {"name": "NovaWave", "desc": "A real-time chat application built to facilitate instant communication.", "link": "#"},
            {"name": "KSEAB Portal", "desc": "A reliable web portal designed to securely display exam results.", "link": "#"}
        ],
        "visitors": [] 
    }
    if not os.path.exists(DATA_FILE): return default_data
    with open(DATA_FILE, "r") as f:
        try:
            data = json.load(f)
            for key in default_data:
                if key not in data: data[key] = default_data[key]
            return data
        except json.JSONDecodeError:
            return default_data

def save_data(data):
    with open(DATA_FILE, "w") as f: json.dump(data, f)

@app.route("/")
def home():
    # The frontend JavaScript now handles device tracking.
    # We just serve the HTML page normally here.
    data = load_data()
    return render_template("index2.html", data=data)

# --- NEW ROUTE: RECEIVE DATA FROM JS ---
@app.route("/log_visitor", methods=["POST"])
def log_visitor():
    try:
        client_data = request.json
        if not client_data:
            return jsonify({"status": "error"}), 400

        data = load_data()
        
        # Get IP address securely
        ip_addr = request.headers.get('X-Forwarded-For', request.remote_addr)
        if ip_addr: ip_addr = ip_addr.split(',')[0]
        else: ip_addr = "Unknown"
        
        visitor_info = {
            "time": datetime.now().strftime("%Y-%m-%d %I:%M %p"),
            "ip": ip_addr,
            "os": client_data.get("os", "Unknown OS"),
            "browser": client_data.get("browser", "Unknown Browser"),
            "device": client_data.get("device", "Unknown Device"),
            "type": client_data.get("type", "Unknown")
        }
        
        # Add to top of list and save
        data["visitors"].insert(0, visitor_info)
        data["visitors"] = data["visitors"][:100] 
        save_data(data)
        
        return jsonify({"status": "success"})
    except Exception as e:
        print("JS Tracker Error:", e)
        return jsonify({"status": "error"}), 500

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST" and "password" in request.form:
        if request.form["password"] == "SUMANM0405":
            session["admin_logged_in"] = True
            return redirect(url_for("admin"))
        else:
            return "Incorrect Password! Try again.", 401

    if not session.get("admin_logged_in"):
        return render_template("admin.html", logged_in=False)

    data = load_data()
    
    if request.method == "POST" and "about_text" in request.form:
        data["about_text"] = request.form.get("about_text")
        data["insta_link"] = request.form.get("insta_link")
        data["focus_1_title"] = request.form.get("focus_1_title")
        data["focus_1_desc"] = request.form.get("focus_1_desc")
        data["focus_1_link"] = request.form.get("focus_1_link")
        data["focus_2_title"] = request.form.get("focus_2_title")
        data["focus_2_desc"] = request.form.get("focus_2_desc")
        data["focus_2_link"] = request.form.get("focus_2_link")
        save_data(data)
        return redirect(url_for("admin"))

    return render_template("admin.html", logged_in=True, data=data)

@app.route("/add_project", methods=["POST"])
def add_project():
    if not session.get("admin_logged_in"): return redirect(url_for("admin"))
    data = load_data()
    data["projects"].append({
        "name": request.form.get("name", "New Project"),
        "desc": request.form.get("desc", ""),
        "link": request.form.get("link", "#")
    })
    save_data(data)
    return redirect(url_for("admin"))

@app.route("/delete_project/<int:idx>", methods=["POST"])
def delete_project(idx):
    if not session.get("admin_logged_in"): return redirect(url_for("admin"))
    data = load_data()
    if 0 <= idx < len(data["projects"]):
        data["projects"].pop(idx)
        save_data(data)
    return redirect(url_for("admin"))

@app.route("/delete_logs", methods=["POST"])
def delete_logs():
    if not session.get("admin_logged_in"): return redirect(url_for("admin"))
    data = load_data()
    data["visitors"] = [] 
    save_data(data)
    return redirect(url_for("admin"))

@app.route("/logout")
def logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
