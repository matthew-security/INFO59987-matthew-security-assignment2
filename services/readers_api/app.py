"""Readers API: serves library readers from readers.txt."""
import logging
from flask import Flask, jsonify

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)
READERS_FILE = "readers.txt"


def load_readers():
    """Read readers.txt and return the readers as a list of dictionaries."""
    readers = []
    with open(READERS_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            reader_id, name, membership = line.split(",")
            readers.append({"id": int(reader_id), "name": name, "membership": membership})
    return readers


@app.route("/")
def home():
    """Simple route to confirm the API is running."""
    return jsonify({"message": "Readers API is running"})


@app.route("/health")
def health():
    """Used by the Docker healthcheck."""
    return jsonify({"status": "healthy"}), 200


@app.route("/readers")
def get_readers():
    """Return every reader in the file."""
    readers = load_readers()
    logger.info("GET /readers returned %d readers", len(readers))
    return jsonify(readers)


@app.route("/readers/<int:reader_id>")
def get_reader(reader_id):
    """Return one reader by id, or a 404 error if it does not exist."""
    for reader in load_readers():
        if reader["id"] == reader_id:
            logger.info("GET /readers/%d found: %s", reader_id, reader["name"])
            return jsonify(reader)
    logger.warning("GET /readers/%d not found", reader_id)
    return jsonify({"error": "Reader not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # nosec B104
