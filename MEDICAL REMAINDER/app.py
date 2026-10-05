
from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key="medical_reminder"

from datetime import datetime
from datetime import date

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("medical.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO users (name, email, password)
        VALUES (?, ?, ?)
        """, (name, email, password))

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("medical.db")
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM users
        WHERE email=? AND password=?
        """, (email, password))

        user = cursor.fetchone()

        conn.close()

        if user:
            session["user"]=user[1]
            return redirect("/dashboard")
        else:
            return "Invalid Email or Password"

    return render_template("login.html")


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return render_template("dashboard.html")


# ---------------- ADD MEDICINE ----------------
@app.route("/add_medicine", methods=["GET", "POST"])
def add_medicine():

    if request.method == "POST":

        medicine_name = request.form["medicine_name"]
        dosage = request.form["dosage"]
        medicine_time = request.form["medicine_time"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]

        conn = sqlite3.connect("medical.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO medicines
        (medicine_name, dosage, medicine_time, start_date, end_date)
        VALUES (?, ?, ?, ?, ?)
        """, (
            medicine_name,
            dosage,
            medicine_time,
            start_date,
            end_date
        ))

        conn.commit()
        conn.close()

        return redirect("/view_medicines")

    return render_template("add_medicine.html")



# ---------------- VIEW MEDICINES ----------------
@app.route("/view_medicines")
def view_medicines():

    delete_expired_medicines()

    conn = sqlite3.connect("medical.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM medicines")
    medicines = cursor.fetchall()

    conn.close()

    return render_template("view_medicines.html", medicines=medicines)

def delete_expired_medicines():

    conn = sqlite3.connect("medical.db")
    cursor = conn.cursor()

    current_date = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M")

    cursor.execute("""
    DELETE FROM medicines
    WHERE
        (end_date < ?)
        OR
        (end_date = ? AND medicine_time <= ?)
    """, (current_date, current_date, current_time))

    conn.commit()
    conn.close()
@app.route("/reminder_settings", methods=["GET", "POST"])
def reminder_settings():

    if request.method == "POST":
        return redirect("/dashboard")

    return render_template("reminder_settings.html")
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/ai_assistant", methods=["GET", "POST"])
def ai_assistant():

    answer = ""

    if request.method == "POST":

        medicine = request.form["question"].lower()

        if medicine == "paracetamol":
            answer = "Paracetamol is used to reduce fever and relieve mild to moderate pain."

        elif medicine == "dolo":
            answer = "Dolo 650 is used to reduce fever and relieve body pain."

        elif medicine == "crocin":
            answer = "Crocin is used to treat fever, headache, and body pain."

        elif medicine == "vitamin c":
            answer = "Vitamin C helps improve immunity."

        elif medicine == "amoxicillin":
            answer = "Amoxicillin is an antibiotic used to treat bacterial infections."

        elif medicine == "cetirizine":
            answer = "Cetirizine is used to treat allergies."

        elif medicine == "ibuprofen":
            answer = "Ibuprofen is used to reduce pain, fever, and inflammation."

        else:
            answer = "Sorry! I don't have information about this medicine."

    return render_template("ai_assistant.html", answer=answer)

if __name__ == "__main__":
    delete_expired_medicines()
    app.run(host="0.0.0.0",port=5000,debug=True)