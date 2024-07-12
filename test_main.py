import pytest
from main import app, db, Book, Author, Genre
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' 
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Crear datos de prueba
            author = Author(Name="Author Test")
            genre = Genre(Name="Genre Test")
            db.session.add(author)
            db.session.add(genre)
            db.session.commit()
            book = Book(Title="Test Book", Isbn="1234567890123", Price=9.99, Quantity=10, Author_id=author.idAuthor, Genre_id=genre.idGenre)
            db.session.add(book)
            db.session.commit()
        yield client
        with app.app_context():
            db.drop_all()

def test_get_main(client):
    response = client.get('/')
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data['message'] == 'hola'

'''
def test_get_books(client):
    response = client.get('/books')
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data) == 1
    assert json_data[0]['title'] == 'Test Book'

def test_get_book_by_id(client):
    response = client.get('/books/1')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['title'] == 'Test Book'

def test_get_book_by_invalid_id(client):
    response = client.get('/books/999')
    assert response.status_code == 404
    json_data = response.get_json()
    assert json_data['message'] == 'book not found'

def test_create_book(client):
    new_book = {
        "Title": "New Book",
        "Isbn": "9876543210987",
        "Price": 15.99,
        "Quantity": 5,
        "Author_id": 1,
        "Genre_id": 1
    }
    response = client.post('/books', data=json.dumps(new_book), content_type='application/json')
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data['title'] == 'New Book'

def test_delete_book(client):
    response = client.delete('/books/1')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['message'] == 'book deleted!'

    # Verifica que el libro haya sido eliminado
    response = client.get('/books/1')
    assert response.status_code == 404

def test_get_books_by_genre(client):
    response = client.get('/books/1/genre')
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data) == 1
    assert json_data[0]['book_title'] == 'Test Book'
'''
