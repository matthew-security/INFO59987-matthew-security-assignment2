"""Staff API: serves library staff from staff.txt."""
import logging
from flask import Flask, jsonify

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)
STAFF_FILE = "staff.txt"


def load_staff():
    """Read staff.txt and return the staff as a list of dictionaries."""
    staff = []
    with open(STAFF_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            staff_id, name, role = line.split(",")
            staff.append({"id": int(staff_id), "name": name, "role": role})
    return staff


@app.route("/")
def home():
    """Simple route to confirm the API is running."""
    return jsonify({"message": "Staff API is running"})


@app.route("/health")
def health():
    """Used by the Docker healthcheck."""
    return jsonify({"status": "healthy"}), 200


@app.route("/staff")
def get_staff():
    """Return every staff member in the file."""
    staff = load_staff()
    logger.info("GET /staff returned %d people", len(staff))
    return jsonify(staff)


@app.route("/staff/<int:staff_id>")
def get_staff_member(staff_id):
    """Return one staff member by id, or a 404 error if it does not exist."""
    for person in load_staff():
        if person["id"] == staff_id:
            logger.info("GET /staff/%d found: %s", staff_id, person["name"])
            return jsonify(person)
    logger.warning("GET /staff/%d not found", staff_id)
    return jsonify({"error": "Staff member not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # nosec B104
