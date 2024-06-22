from flask import Flask, request, jsonify
import requests
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)

books = []
ratings = {}

# MongoDB configuration
mongo_client = MongoClient('mongodb://mongodb:27017/')
db = mongo_client['bookshop']
books_collection = db['books']
ratings_collection = db['ratings']


# Helper function to generate unique IDs
def generate_id():
    #return str(len(books) + 1)
    return str(ObjectId())

def fetch_book_info(isbn):
    google_books_url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}'
    response = requests.get(google_books_url)

    if response.status_code == 200:
        try:
            google_books_data = response.json()['items'][0]['volumeInfo']
            book_name = google_books_data.get("title", "missing")

            # Handle authors field
            authors = google_books_data.get("authors", [])
            if len(authors) == 1:
                author_name = authors[0]
            elif len(authors) > 1:
                author_name = " and ".join(authors)
            else:
                author_name = "missing"

            published_date = google_books_data.get("publishedDate", "missing")
            publisher = google_books_data.get("publisher", "missing")


            # Format published date
            if len(published_date) == 4:  # If only year is provided
                published_date = f"{published_date}-01-01"
            elif len(published_date) != 10:  # If not in YYYY-MM-DD format
                published_date = "missing"


            book_info = {
                "authors": author_name,
                "publisher": publisher,
                "publishedDate": published_date,
            }
            return book_info
        except (IndexError, KeyError):
            return None  # No items found in Google Books API response
    else:
        return None  # Error fetching data from Google Books API


# Endpoint for creating a new book
@app.route('/books', methods=['POST'])
def create_book():
    data = request.json
    if request.headers['Content-Type'] != 'application/json':
        return jsonify({"error": "Unsupported media type"}), 415

    if 'title' not in data or 'ISBN' not in data or 'genre' not in data:
        return jsonify({"error": "Missing required fields"}), 422

    accepted_genres = ["Fiction", "Children", "Biography", "Science", "Science Fiction", "Fantasy", "Other"]
    if data['genre'] not in accepted_genres:
        return jsonify({"error": "Genre is not one of the accepted values"}), 422

    # Check if a book with the same ISBN already exists
    existing_book = books_collection.find_one({"ISBN": data['ISBN']})
    if existing_book:
        return jsonify({"error": "A book with this ISBN number already exists"}), 422

    book_info = fetch_book_info(data['ISBN'])
    if book_info is None:
        return jsonify({"error": "Unable to connect to Google"}), 500

    if not book_info:
        return jsonify({"error": "No information available from Google Books API for given ISBN number"}), 422

    book = {
        "title": data['title'],
        "ISBN": data['ISBN'],
        "genre": data['genre'],
        **book_info
    }

    result = books_collection.insert_one(book)
    book_id = str(result.inserted_id)

    ratings_collection.insert_one({
        "_id": ObjectId(book_id),
        "values": [],
        "average": 0,
        "title": data['title']
    })

    return jsonify({"ID": str(book_id)}), 201



@app.route('/books', methods=['GET'])
def get_books():
    query_params = request.args.to_dict()
    query = {}
    # Filter books based on query string
    for key, value in query_params.items():
        query[key] = value

    filtered_books = list(books_collection.find(query))
    response = []
    for book in filtered_books:
        book['id'] = str(book.pop('_id'))  # Rename _id to id and convert to string
        response.append(book)

    return jsonify(response)


# Endpoint for retrieving, updating, or deleting a specific book
@app.route('/books/<book_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_book(book_id):
    try:
        book_id = ObjectId(book_id)
    except:
        return jsonify({"error": "Invalid book ID"}), 400

    book = books_collection.find_one({"_id": book_id})
    if not book:
        return jsonify({"error": "Book not found"}), 404

    if request.method == 'GET':
        book['_id'] = str(book['_id'])
        return jsonify(book)

    elif request.method == 'PUT':
        data = request.json
        required_fields = ['title', 'ISBN', 'genre', 'authors', 'publisher', 'publishedDate']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 422

        update_data = {field: data[field] for field in required_fields}

        books_collection.update_one({"_id": book_id}, {"$set": update_data})
        return jsonify({"ID": str(book_id)}), 200

    elif request.method == 'DELETE':
        books_collection.delete_one({"_id": book_id})
        ratings_collection.delete_one({"_id": book_id})
        return jsonify({"ID": str(book_id)}), 200


# Endpoint for adding a new rating for a book
@app.route('/ratings/<book_id>/values', methods=['POST'])
def add_rating(book_id):
    try:
        book_id = ObjectId(book_id)
    except:
        return jsonify({"error": "Invalid book ID"}), 400
    data = request.json
    if 'value' not in data or data['value'] not in [3, 4, 5]:
        return jsonify({"error": "Invalid rating value"}), 422
    rating_doc = ratings_collection.find_one({"_id": book_id})
    if not rating_doc:
        return jsonify({"error": "Rating document not found"}), 404
    ratings_collection.update_one(
        {"_id": book_id},
        {"$push": {"values": data['value']}}
    )
    rating_doc = ratings_collection.find_one({"_id": book_id})
    average_rating = sum(rating_doc["values"]) / len(rating_doc["values"])
    ratings_collection.update_one(
        {"_id": book_id},
        {"$set": {"average": round(average_rating, 2)}}
    )
    return jsonify({"average": round(average_rating, 2)}), 200

# Endpoint for retrieving ratings for a specific book
@app.route('/ratings/<book_id>', methods=['GET'])
def get_rating_by_id(book_id):
    try:
        book_id = ObjectId(book_id)
    except:
        return jsonify({"error": "Invalid book ID"}), 400

    rating_doc = ratings_collection.find_one({"_id": book_id})
    if not rating_doc:
        return jsonify({"error": "Book not found"}), 404

    rating_doc['_id'] = str(rating_doc['_id'])
    return jsonify(rating_doc), 200

# Endpoint for retrieving all ratings or filtering by book ID
@app.route('/ratings', methods=['GET'])
def get_ratings():
    all_ratings = list(ratings_collection.find())
    for rating in all_ratings:
        rating['_id'] = str(rating['_id'])
    return jsonify(all_ratings), 200

# Endpoint for retrieving the top-rated books
@app.route('/top', methods=['GET'])
def get_top_books():
    top_books = list(ratings_collection.find().sort("average", -1).limit(3))
    response = []

    for book in top_books:
        book_id = str(book.pop('_id'))  # Convert _id to string and rename to id
        response.append({
            "id": book_id,  # Use 'id' as the key for the response
            "title": book.get("title", ""),
            "average": book.get("average", 0)
        })

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('BOOKSHOP_SERVICE_PORT', '8000')), debug=True)
