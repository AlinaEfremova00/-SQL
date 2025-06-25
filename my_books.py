from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine("sqlite:///my_books.db")


class Base(DeclarativeBase):
    pass


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year = Column(Integer)

    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', author='{self.author}', year={self.year})>"


Base.metadata.create_all(bind=engine)
print("База данных и таблица созданы")


Session = sessionmaker(bind=engine)
session = Session()


def add_book(title, author, year=None):
    new_book = Book(title=title, author=author, year=year)
    session.add(new_book)
    session.commit()
    print(f"Книга '{title}' успешно добавлена!")


def get_all_books():

    books = session.query(Book).all()
    if books:
        print("Список всех книг:")
        for book in books:
            print(f"ID: {book.id}, Название: {book.title}, Автор: {book.author}, Год: {book.year}")
    else:
        print("В базе данных нет книг.")


def find_book_by_title(title):
    book = session.query(Book).filter_by(title=title).first()
    if book:
        print(f"Найдена книга: ID: {book.id}, Название: {book.title}, Автор: {book.author}, Год: {book.year}")
    else:
        print(f"Книга с названием '{title}' не найдена.")


def update_book_year(title, new_year):
    book = session.query(Book).filter_by(title=title).first()
    if book:
        book.year = new_year
        session.commit()
        print(f"Год издания книги '{title}' обновлен на {new_year}.")
    else:
        print(f"Книга с названием '{title}' не найдена.")


def delete_book_by_id(book_id):
    book = session.query(Book).filter_by(id=book_id).first()
    if book:
        session.delete(book)
        session.commit()
        print(f"Книга с ID {book_id} удалена.")
    else:
        print(f"Книга с ID {book_id} не найдена.")


add_book("Три товарища", "Ремарк", 1936)
get_all_books()
find_book_by_title("Три товарища")
update_book_year("Три товарища", 1945)
delete_book_by_id(1)
get_all_books()

session.close()
