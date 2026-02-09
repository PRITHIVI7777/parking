from flask import Flask, render_template, request
import sqlite3
from vehicle_data import vehicle_dimensions, vehicle_type_map

app = Flask(__name__)

# Database connection
def get_db():
    return sqlite3.connect("parking.db")

# AI slot calculation
def calculate_required_size(length, width):
    return length * 1.1, width * 1.1  # 10% buffer

# Slot allocation logic
def allocate_slot(user_type, vehicle_type, req_len, req_wid):
    """Try several allocation strategies in order:
    1) Exact fit (with buffer)
    2) Swap length/width (orientation)
    3) Relax sizes (5% smaller requirement)
    4) Fallback: any free slot for the zone/type (last resort)

    Returns (slot_no, note) where note can be None or a short explanation.
    """
    db = get_db()
    cur = db.cursor()

    queries = []
    # exact fit
    queries.append(("SELECT slot_no FROM parking_slots WHERE zone=? AND vehicle_type=? AND status='FREE' AND length>=? AND width>=? ORDER BY length, width LIMIT 1", (user_type, vehicle_type, req_len, req_wid), None))
    # swapped orientation
    queries.append(("SELECT slot_no FROM parking_slots WHERE zone=? AND vehicle_type=? AND status='FREE' AND length>=? AND width>=? ORDER BY length, width LIMIT 1", (user_type, vehicle_type, req_wid, req_len), 'Found by swapping length/width (orientation)'))
    # relaxed sizes (5% smaller requirements)
    relaxed_len = req_len * 0.95
    relaxed_wid = req_wid * 0.95
    queries.append(("SELECT slot_no FROM parking_slots WHERE zone=? AND vehicle_type=? AND status='FREE' AND length>=? AND width>=? ORDER BY length, width LIMIT 1", (user_type, vehicle_type, relaxed_len, relaxed_wid), 'Found by relaxing size constraints'))
    # final fallback: any free slot in zone/type
    queries.append(("SELECT slot_no FROM parking_slots WHERE zone=? AND vehicle_type=? AND status='FREE' ORDER BY length DESC LIMIT 1", (user_type, vehicle_type), 'Fallback: slot selected ignoring size checks'))

    for sql, params, note in queries:
        cur.execute(sql, params)
        slot = cur.fetchone()
        if slot:
            cur.execute("UPDATE parking_slots SET status='BOOKED' WHERE slot_no=?", (slot[0],))
            db.commit()
            return slot[0], note

    return None, None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_id = request.form["user_id"]
        role = request.form["role"]  # student / staff
        vehicle_type = request.form["vehicle_type"]
        model = request.form["model"]

        models_items = [{"name": m, "type": vehicle_type_map.get(m, "car")} for m in vehicle_dimensions.keys()]
        if model not in vehicle_dimensions:
            return render_template("login.html", error=f"Vehicle model '{model}' not found! Please select from available models.", models=list(vehicle_dimensions.keys()), models_items=models_items)

        # Validate that the selected model matches the chosen vehicle_type
        model_type = vehicle_type_map.get(model)
        if model_type and model_type != vehicle_type:
            return render_template("login.html", error=f"Selected model '{model}' is a {model_type} but you selected '{vehicle_type}'. Please correct the selection.", models=list(vehicle_dimensions.keys()), models_items=models_items)

        length, width = vehicle_dimensions[model]
        req_len, req_wid = calculate_required_size(length, width)

        slot, note = allocate_slot(role, vehicle_type, req_len, req_wid)

        if slot:
            # pass an informational note to the result page if allocation used a fallback
            return render_template("result.html", slot=slot, note=note)
        else:
            return render_template("login.html", error="No parking slot available for your vehicle type!", models=list(vehicle_dimensions.keys()), models_items=models_items)

    # pass models with their type for template rendering
    models_items = [{"name": m, "type": vehicle_type_map.get(m, "car")} for m in vehicle_dimensions.keys()]
    return render_template("login.html", models=list(vehicle_dimensions.keys()), models_items=models_items)

if __name__ == "__main__":
    app.run(debug=True)
