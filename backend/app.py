import os
import time

from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app)

# ---- DB config from environment (set via Kubernetes Secret/ConfigMap) ----
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "mysql"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "tripuser"),
    "password": os.getenv("DB_PASSWORD", "trippass"),
    "database": os.getenv("DB_NAME", "tripdb"),
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def init_db(retries=10, delay=5):
    """Wait for MySQL to be ready, then create the trips table."""
    for attempt in range(1, retries + 1):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS trips (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    destination VARCHAR(255) NOT NULL,
                    start_date DATE NOT NULL,
                    end_date DATE NOT NULL,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.commit()
            cur.close()
            conn.close()
            print("Database initialized.")
            return
        except Error as e:
            print(f"DB not ready (attempt {attempt}/{retries}): {e}")
            time.sleep(delay)
    raise RuntimeError("Could not connect to the database after retries.")


@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/api/trips", methods=["GET"])
def list_trips():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM trips ORDER BY start_date")
    rows = cur.fetchall()
    # Convert dates to ISO strings
    for r in rows:
        r["start_date"] = r["start_date"].isoformat()
        r["end_date"] = r["end_date"].isoformat()
        if r.get("created_at"):
            r["created_at"] = r["created_at"].isoformat()
    cur.close()
    conn.close()
    return jsonify(rows)


@app.route("/api/trips", methods=["POST"])
def add_trip():
    data = request.get_json(force=True)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO trips (destination, start_date, end_date, notes) VALUES (%s, %s, %s, %s)",
        (data["destination"], data["start_date"], data["end_date"], data.get("notes", "")),
    )
    conn.commit()
    new_id = cur.lastrowid
    cur.close()
    conn.close()
    return jsonify({"id": new_id, "message": "created"}), 201


@app.route("/api/trips/<int:trip_id>", methods=["DELETE"])
def delete_trip(trip_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM trips WHERE id = %s", (trip_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "deleted"})


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)

