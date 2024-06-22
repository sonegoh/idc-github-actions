import requests

BASE_URL = "http://localhost:5001"

book1 = {
    "title": "Adventures of Huckleberry Finn",
    "ISBN": "9780520343641",
    "genre": "Fiction"
}

book2 = {
    "title": "The Best of Isaac Asimov",
    "ISBN": "9780385050784",
    "genre": "Science Fiction"
}

book3 = {
    "title": "Fear No Evil",
    "ISBN": "9780394558783",
    "genre": "Biography"
}

book4 = {
    "title": "No such book",
    "ISBN": "0000001111111",
    "genre": "Biography"
}

book5 = {
    "title": "The Greatest Joke Book Ever",
    "authors": "Mel Greene",
    "ISBN": "9780380798490",
    "genre": "Jokes"
}


def test_create_books():
    response1 = requests.post(f"{BASE_URL}/books", json=book1)
    response2 = requests.post(f"{BASE_URL}/books", json=book2)
    response3 = requests.post(f"{BASE_URL}/books", json=book3)

    assert response1.status_code == 201
    assert response2.status_code == 201
    assert response3.status_code == 201

    book1_id = response1.json()["ID"]
    book2_id = response2.json()["ID"]
    book3_id = response3.json()["ID"]

    assert book1_id != book2_id
    assert book1_id != book3_id
    assert book2_id != book3_id

    return book1_id, book2_id, book3_id


def test_get_book1(book1_id):
    response = requests.get(f"{BASE_URL}/books/{book1_id}")
    data = response.json()

    assert response.status_code == 200
    assert data["authors"] == "Mark Twain"


def test_get_all_books():
    response = requests.get(f"{BASE_URL}/books")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 3


def test_create_invalid_book():
    response = requests.post(f"{BASE_URL}/books", json=book4)

    assert response.status_code == 500


def test_delete_book2(book2_id):
    response = requests.delete(f"{BASE_URL}/books/{book2_id}")

    assert response.status_code == 200


def test_get_deleted_book2(book2_id):
    response = requests.get(f"{BASE_URL}/books/{book2_id}")

    assert response.status_code == 404


def test_create_book_with_invalid_genre():
    response = requests.post(f"{BASE_URL}/books", json=book5)

    assert response.status_code == 422


if __name__ == "__main__":
    book1_id, book2_id, book3_id = test_create_books()
    test_get_book1(book1_id)
    test_get_all_books()
    test_create_invalid_book()
    test_delete_book2(book2_id)
    test_get_deleted_book2(book2_id)
    test_create_book_with_invalid_genre()
