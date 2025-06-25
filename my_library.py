from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, DeclarativeBase, relationship

engine = create_engine("sqlite:///my_library.db")


class Base(DeclarativeBase):
    pass


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year = Column(Integer, nullable=True)
    publisher = relationship("Publisher", back_populates="book", uselist=False)
    reviews = relationship("Review", back_populates="book")
    authors = relationship("Author", secondary="book_author", back_populates="books")

    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', author='{self.author}', year={self.year})>"


class Publisher(Base):
    __tablename__ = 'publishers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), unique=True)
    book = relationship("Book", back_populates="publisher")

    def __repr__(self):
        return f"<Publisher(id={self.id}, name='{self.name}', book_id={self.book_id})>"


class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'))
    book = relationship("Book", back_populates="reviews")

    def __repr__(self):
        return f"<Review(id={self.id}, text='{self.text}', book_id={self.book_id})>"


book_author = Table(
    'book_author', Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id')),
    Column('author_id', Integer, ForeignKey('authors.id'))
)


class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    books = relationship("Book", secondary="book_author", back_populates="authors")

    def __repr__(self):
        return f"<Author(id={self.id}, name='{self.name}')>"


Base.metadata.create_all(bind=engine)
print("База данных и таблицы созданы")


Session = sessionmaker(bind=engine)
session = Session()


def add_book_with_publisher(title, author, publisher_name, year=None):
    new_book = Book(title=title, author=author, year=year)
    new_publisher = Publisher(name=publisher_name, book=new_book)
    session.add(new_book)
    session.add(new_publisher)
    session.commit()
    print(f"Книга '{title}' с издательством '{publisher_name}' успешно добавлена!")


def add_review_to_book(book_id, review_text):
    book = session.query(Book).filter_by(id=book_id).first()
    if book:
        new_review = Review(text=review_text, book=book)
        session.add(new_review)
        session.commit()
        print(f"Отзыв к книге '{book.title}' успешно добавлен!")
    else:
        print(f"Книга с ID {book_id} не найдена.")


def get_book_with_reviews(book_id):
    book = session.query(Book).filter_by(id=book_id).first()
    if book:
        print(f"Книга: {book.title}, Автор: {book.author}, Год: {book.year}")
        if book.reviews:
            print("Отзывы:")
            for review in book.reviews:
                print(f"  - {review.text}")
        else:
            print("Отзывов нет.")
    else:
        print(f"Книга с ID {book_id} не найдена.")


def add_author_to_book(book_id, author_name):
    book = session.query(Book).filter_by(id=book_id).first()
    if book:
        new_author = Author(name=author_name)
        book.authors.append(new_author)
        session.add(new_author)
        session.commit()
        print(f"Автор '{author_name}' успешно добавлен к книге '{book.title}'!")
    else:
        print(f"Книга с ID {book_id} не найдена.")


def get_book_with_authors(book_id):
    book = session.query(Book).filter_by(id=book_id).first()
    if book:
        print(f"Книга: {book.title}, Автор: {book.author}, Год: {book.year}")
        if book.authors:
            print("Авторы:")
            for author in book.authors:
                print(f"  - {author.name}")
        else:
            print("Авторов нет.")
    else:
        print(f"Книга с ID {book_id} не найдена.")


add_book_with_publisher("Гарри Поттер", "Джоан Роулинг", "Блумсбери", 1997)
add_review_to_book(1, "Магия и приключения!")
add_author_to_book(1, "Джоан Роулинг")
get_book_with_reviews(1)
get_book_with_authors(1)
session.close()
