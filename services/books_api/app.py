"""Library API: a small Flask app that serves books from books.txt."""
import logging
from flask import Flask, jsonify

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)
BOOKS_FILE = "books.txt"


def load_books():
    """Read books.txt and return the books as a list of dictionaries."""
    books = []
    with open(BOOKS_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            book_id, title, author, status = line.split(",")
            books.append({"id": int(book_id), "title": title, "author": author, "status": status})
    return books


@app.route("/")
def home():
    """Simple route to confirm the API is running."""
    return jsonify({"message": "Library API is running"})


@app.route("/books")
def get_books():
    """Return every book in the file."""
    books = load_books()
    logger.info("GET /books returned %d books", len(books))
    return jsonify(books)


@app.route("/books/<int:book_id>")
def get_book(book_id):
    """Return one book by id, or a 404 error if it does not exist."""
    for book in load_books():
        if book["id"] == book_id:
            logger.info("GET /books/%d found: %s", book_id, book["title"])
            return jsonify(book)
    logger.warning("GET /books/%d not found", book_id)
    return jsonify({"error": "Book not found"}), 404


@app.route("/health")
def health():
    """Used by the Docker healthcheck."""
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    # Listening on all interfaces is required so the container is reachable.
    app.run(host="0.0.0.0", port=5000)  # nosec B104
