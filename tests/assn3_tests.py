# import pytest
# import requests

# BASE_URL = "http://localhost:5001"

# books = [
#     {
#         "title": "Adventures of Huckleberry Finn",
#         "ISBN": "9780520343641",
#         "genre": "Fiction"
#     },
#     {
#         "title": "The Best of Isaac Asimov",
#         "ISBN": "9780385050784",
#         "genre": "Science Fiction"
#     },
#     {
#         "title": "Fear No Evil",
#         "ISBN": "9780394558783",
#         "genre": "Biography"
#     },
#     {
#         "title": "No such book",
#         "ISBN": "0000001111111",
#         "genre": "Biography"
#     },
#     {
#         "title": "The Greatest Joke Book Ever",
#         "authors": "Mel Greene",
#         "ISBN": "9780380798490",
#         "genre": "Jokes"
#     },
#     {
#         "title": "The Adventures of Tom Sawyer",
#         "ISBN": "9780195810400",
#         "genre": "Fiction"
#     },
#     {
#         "title": "I, Robot",
#         "ISBN": "9780553294385",
#         "genre": "Science Fiction"
#     },
#     {
#         "title": "Second Foundation",
#         "ISBN": "9780553293364",
#         "genre": "Science Fiction"
#     }
# ]


# @pytest.fixture(scope="module")
# def create_books():
#     book_ids = []
#     for book in books[:3]:  # Create only the first three valid books
#         response = requests.post(f"{BASE_URL}/books", json=book)
#         assert response.status_code == 201
#         book_ids.append(response.json()["ID"])
#     assert len(set(book_ids)) == 3  # Ensure all IDs are unique
#     return book_ids


# @pytest.fixture
# def book1_id(create_books):
#     return create_books[0]


# @pytest.fixture
# def book2_id(create_books):
#     return create_books[1]


# @pytest.fixture
# def book3_id(create_books):
#     return create_books[2]


# def test_get_book1(book1_id):
#     response = requests.get(f"{BASE_URL}/books/{book1_id}")
#     data = response.json()

#     assert response.status_code == 200
#     assert data["authors"] == "Mark Twain"


# def test_get_all_books():
#     response = requests.get(f"{BASE_URL}/books")
#     data = response.json()

#     assert response.status_code == 200
#     assert len(data) == 3  # Ensure there are 3 books


# def test_create_invalid_book():
#     response = requests.post(f"{BASE_URL}/books", json=books[3])

#     assert response.status_code in [400, 500]


# def test_delete_book2(book2_id):
#     response = requests.delete(f"{BASE_URL}/books/{book2_id}")

#     assert response.status_code == 200


# def test_get_deleted_book2(book2_id):
#     response = requests.get(f"{BASE_URL}/books/{book2_id}")

#     assert response.status_code == 404


# def test_create_book_with_invalid_genre():
#     response = requests.post(f"{BASE_URL}/books", json=books[4])

#     assert response.status_code == 422

# ----- NIR TEST ------ 

import requests

BASE_URL = "http://localhost:5001/books"

book6 = {
    "title": "The Adventures of Tom Sawyer",
    "ISBN": "9780195810400",
    "genre": "Fiction"
}

book7 = {
    "title": "I, Robot",
    "ISBN": "9780553294385",
    "genre": "Science Fiction"
}

book8 = {
    "title": "Second Foundation",
    "ISBN": "9780553293364",
    "genre": "Science Fiction"
}

books_data = []


def test_post_books():
    books = [book6, book7, book8]
    for book in books:
        res = requests.post(BASE_URL, json=book)
        assert res.status_code == 201
        res_data = res.json()
        assert "ID" in res_data
        books_data.append(res_data)
        books_data_tuples = [frozenset(book.items()) for book in books_data]
    assert len(set(books_data_tuples)) == 3


def test_get_query():
    res = requests.get(f"{BASE_URL}?authors=Isaac Asimov")
    assert res.status_code == 200
    assert len(res.json()) == 2


def test_delete_book():
    res = requests.delete(f"{BASE_URL}/{books_data[0]['ID']}")
    assert res.status_code == 200


def test_post_book():
    book = {
        "title": "The Art of Loving",
        "ISBN": "9780062138927",
        "genre": "Science"
    }
    res = requests.post(BASE_URL, json=book)
    assert res.status_code == 201



def test_get_new_book_query():
    res = requests.get(f"{BASE_URL}?genre=Science")
    assert res.status_code == 200
    res_data = res.json()
    assert res_data[0]["title"] == "The Art of Loving"
