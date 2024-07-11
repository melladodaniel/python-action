from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:password@172.17.0.2/book-inventory"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

### Models ###

class Book(db.Model):
    idBook = db.Column(db.Integer, primary_key = True)
    Title = db.Column(db.String(255), nullable = False)
    Isbn = db.Column(db.String(255), nullable = False)
    Price = db.Column(db.Numeric(10,2), nullable = False)
    Quantity = db.Column(db.Integer, nullable = False)
    Author_id = db.Column(db.Integer, db.ForeignKey('author.idAuthor'), nullable = False)
    author = db.relationship('Author', backref=db.backref('book', lazy = True))
    Genre_id = db.Column(db.Integer, db.ForeignKey('genre.idGenre'), nullable = False)
    genre = db.relationship('Genre', backref=db.backref('book', lazy = True))

    def __repr__(self):
        return f'<Book {self.Title}>'

class Author(db.Model):
    idAuthor = db.Column(db.Integer, primary_key = True)
    Name = db.Column(db.String(255), nullable = False)

    def __repr__(self):
        return f'<Commit {self.Name}>'

class Genre(db.Model):
    idGenre = db.Column(db.Integer, primary_key = True)
    Name = db.Column(db.String(255), nullable = False)

    def __repr__(self):
        return f'<Commit {self.Name}>'

### Routes ###

@app.route('/', methods=['GET'])
def main():
    return jsonify({'message': 'hola'}), 200

@app.route('/books', methods=['GET'])
def getBooks():
    books = Book.query.all()
    books_list = []
    for book in books:
        book_data = {
            "id": book.idBook,
            "title": book.Title,
            "ISBN": book.Isbn,
            "Price": book.Price,
            "Quantity": book.Quantity,
            "Genre id": book.Genre_id,
            "Author id": book.Author_id
        }
        books_list.append(book_data)
    return jsonify(books_list), 200

@app.route('/books/<int:id>', methods=['GET'])
def getBookById(id):
   #book = Book.query.get(id)
    book = db.session.get(Book, id)
    if book is None:
        return jsonify({'message' : 'book not found'}), 404
    book_data = {
            "id": book.idBook,
            "title": book.Title,
            "ISBN": book.Isbn,
            "Price": book.Price,
            "Quantity": book.Quantity,
            "Genre id": book.Genre_id,
            "Author id": book.Author_id
    }
    return jsonify(book_data), 200

@app.route('/books', methods=['POST'])
def createBook():
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Invalid JSON provided"}), 400
    if 'Title' not in data or 'Isbn' not in data or 'Price' not in data or 'Quantity' not in data:
        return jsonify({"error": "Missing data in JSON"}), 400
    new_book = Book(Title=data['Title'], Isbn=data['Isbn'], Price=data['Price'], Quantity=data['Quantity'], Author_id=data['Author_id'], Genre_id=data['Genre_id'])
    try:
        db.session.add(new_book)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
    return jsonify({
            "id": new_book.idBook,
            "title": new_book.Title,
            "ISBN": new_book.Isbn,
            "Price": new_book.Price,
            "Quantity": new_book.Quantity,
            "Genre id": new_book.Genre_id,
            "Author id": new_book.Author_id
    }), 201

@app.route('/books/<int:id>', methods=['DELETE'])
def deleteBook(id):
    # book = Book.query.get(id)
    book = db.session.get(Book, id)
    if book is None:
        return jsonify({'message' : 'book not found'}), 404
    
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message':'book deleted!'}),200

@app.route('/books/<int:id>/genre', methods=['GET'])
def getBooksByGenre(id):
    results = db.session.query(Book, Genre).join(Genre, Genre.idGenre == Book.Genre_id).filter(Genre.idGenre == id).all()
    output = []
    for book, genre in results:
        book_genre_data = {
            'book_id': book.idBook,
            'book_title': book.Title,
            'book_isbn': book.Isbn,
            'genre_id': genre.idGenre,
            'genre_name': genre.Name
        }
        output.append(book_genre_data)
    return jsonify(output), 200


if __name__ == '__main__':
    app.run(port=5555)