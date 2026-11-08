from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=Text)
    name = Column(String, nullable=False)
    biography = Column(Text)

    books = relationship("Book", back_populates="author")


class Gener(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)

    books = relationship("Book", back_populates="genre")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    isbn = Column(String, unique=True)
    publisher = Column(String)
    punlication_year = Column(Integer)
    cover_image = Column(String)
    is_available = Column(Boolean, default=True)

    author_id = Column(Integer, ForeignKey("authors.id"))
    genre_id = Column(Integer, ForeignKey("genres.id"))

    author = relationship("Author", back_populates="books")
    genre = relationship("Genre", back_populates="Books")

