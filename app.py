from flask import Flask, render_template, request
import sqlite3
from vehicle_data import vehicle_dimensions

app = Flask(__name__)

# Database connection
def get_db():
    return sqlite3.connect("parking.db")

# AI slot calculation
def calculate_required_size(length, width):
    return length * 1.1, width * 1.1  # 10% buffer

# Slot allocation logic
def allocate_slot(user_type, vehicle_type, req_len, req_wid):
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        SELECT slot_no FROM parking_slots
        WHERE zone=? AND vehicle_type=? AND status='FREE'
        AND length>=? AND width>=?
        ORDER BY length, width
        LIMIT 1
    """, (user_type, vehicle_type, req_len, req_wid))

    slot = cur.fetchone()

    if slot:
        cur.execute("UPDATE parking_slots SET status='BOOKED' WHERE slot_no=?", (slot[0],))
        db.commit()
        return slot[0]

    return None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_id = request.form["user_id"]
        role = request.form["role"]  # student / staff
        vehicle_type = request.form["vehicle_type"]
        model = request.form["model"]

        if model not in vehicle_dimensions:
            return render_template("login.html", error=f"Vehicle model '{model}' not found! Please select from available models.", models=list(vehicle_dimensions.keys()))

        length, width = vehicle_dimensions[model]
        req_len, req_wid = calculate_required_size(length, width)

        slot = allocate_slot(role, vehicle_type, req_len, req_wid)

        if slot:
            return render_template("result.html", slot=slot)
        else:
            return render_template("login.html", error="No parking slot available for your vehicle type!", models=list(vehicle_dimensions.keys()))

    return render_template("login.html", models=list(vehicle_dimensions.keys()))

if __name__ == "__main__":
    app.run(debug=True)
