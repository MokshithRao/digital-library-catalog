from database import SessionLocal
from models import Author, Genre, Book


def seed_database():
    db = SessionLocal()

    try:
        # -------------------------------
        # 1. INSERT AUTHORS
        # -------------------------------

        author_names = [
            "Héctor García and Francesc Miralles",
            "Paulo Coelho",
            "Khaled Hosseini",
            "John Green",
            "Coltan Scrivner",
            "Hanya Yanagihara",
            "Sam Bhagwat",
            "M. L. Rio",
            "James Clear",
            "Cal Newport",
            "Robert C. Martin",
            "Eric Matthes",
            "Morgan Housel",
            "Yuval Noah Harari",
            "Matt Haig"
        ]

        for name in author_names:
            existing_author = db.query(Author).filter(
                Author.name == name
            ).first()

            if not existing_author:
                db.add(Author(name=name))

        db.commit()
        print("Authors added successfully!")

        # -------------------------------
        # 2. INSERT GENRES
        # -------------------------------

        genre_names = [
            "Self-help",
            "Fiction",
            "Historical Fiction",
            "Young Adult",
            "Literary Fiction",
            "Science",
            "Technology",
            "Mystery",
            "Productivity",
            "Programming",
            "Finance",
            "History"
        ]

        for name in genre_names:
            existing_genre = db.query(Genre).filter(
                Genre.name == name
            ).first()

            if not existing_genre:
                db.add(Genre(name=name))

        db.commit()
        print("Genres added successfully!")

        # -------------------------------
        # 3. RETRIEVE AUTHORS AND GENRES
        # -------------------------------

        authors = {
            author.name: author
            for author in db.query(Author).all()
        }

        genres = {
            genre.name: genre
            for genre in db.query(Genre).all()
        }

        # -------------------------------
        # 4. BOOK DATA
        # -------------------------------

        book_data = [
            {
                "title": "Ikigai",
                "description": "Explores the Japanese concept of ikigai, or finding purpose and meaning in everyday life.",
                "isbn": "9780143130727",
                "publisher": "Penguin Life",
                "publication_year": 2017,
                "author": "Héctor García and Francesc Miralles",
                "genre": "Self-help",
                "cover_image": "ikigai.jpg"
            },
            {
                "title": "The Alchemist",
                "description": "A young shepherd named Santiago travels in search of treasure and discovers the importance of following his dreams.",
                "isbn": "9780062315007",
                "publisher": "HarperOne",
                "publication_year": 2014,
                "author": "Paulo Coelho",
                "genre": "Fiction",
                "cover_image": "the_alchemist.jpg"
            },
            {
                "title": "The Kite Runner",
                "description": "A powerful story of friendship, betrayal, guilt and redemption set against the changing history of Afghanistan.",
                "isbn": "9781594631931",
                "publisher": "Riverhead Books",
                "publication_year": 2013,
                "author": "Khaled Hosseini",
                "genre": "Historical Fiction",
                "cover_image": "the_kite_runner.jpg"
            },
            {
                "title": "Looking for Alaska",
                "description": "Miles Halter enters a boarding school and experiences friendship, love, loss and the uncertainties of growing up.",
                "isbn": "9780525475064",
                "publisher": "Dutton Books for Young Readers",
                "publication_year": 2005,
                "author": "John Green",
                "genre": "Young Adult",
                "cover_image": "looking_for_alaska.jpg"
            },
            {
                "title": "Morbidly Curious: A Scientist Explains Why We Can't Look Away",
                "description": "Behavioral scientist Coltan Scrivner explores morbid curiosity and why humans are drawn to frightening and disturbing subjects.",
                "isbn": "9780593511299",
                "publisher": "Penguin Books",
                "publication_year": 2025,
                "author": "Coltan Scrivner",
                "genre": "Science",
                "cover_image": "morbidly_curious.jpg"
            },
            {
                "title": "A Little Life",
                "description": "Four college friends navigate adulthood, friendship, ambition and trauma in New York City.",
                "isbn": "9780804172707",
                "publisher": "Vintage",
                "publication_year": 2016,
                "author": "Hanya Yanagihara",
                "genre": "Literary Fiction",
                "cover_image": "a_little_life.jpg"
            },
            {
                "title": "Principles of Building AI Agents",
                "description": "A practical guide to AI agents covering language models, prompting, tools, memory, workflows and retrieval-augmented generation.",
                "isbn": "9798312004281",
                "publisher": "Independently Published",
                "publication_year": 2025,
                "author": "Sam Bhagwat",
                "genre": "Technology",
                "cover_image": "principles_of_building_ai_agents.jpg"
            },
            {
                "title": "If We Were Villains",
                "description": "A group of Shakespearean acting students at an elite arts college become entangled in rivalry, obsession and tragedy.",
                "isbn": None,
                "publisher": "Flatiron Books",
                "publication_year": 2017,
                "author": "M. L. Rio",
                "genre": "Mystery",
                "cover_image": "if_we_were_villains.jpg"
            },
            {
                "title": "Atomic Habits",
                "description": "Explains how small behavioral changes and consistent habits can produce remarkable long-term improvements.",
                "isbn": "9781847941831",
                "publisher": "Random House Business",
                "publication_year": 2018,
                "author": "James Clear",
                "genre": "Self-help",
                "cover_image": "atomic_habits.jpg"
            },
            {
                "title": "Deep Work",
                "description": "Explores the value of focused, distraction-free work and provides strategies for developing concentration.",
                "isbn": "9781455586691",
                "publisher": "Grand Central Publishing",
                "publication_year": 2016,
                "author": "Cal Newport",
                "genre": "Productivity",
                "cover_image": "deep_work.jpg"
            },
            {
                "title": "Clean Code",
                "description": "Introduces principles and practices for writing readable, maintainable and well-structured software.",
                "isbn": None,
                "publisher": "Prentice Hall",
                "publication_year": 2008,
                "author": "Robert C. Martin",
                "genre": "Programming",
                "cover_image": "clean_code.jpg"
            },
            {
                "title": "Python Crash Course",
                "description": "A hands-on introduction to Python programming covering fundamentals and practical projects.",
                "isbn": "9781718502703",
                "publisher": "No Starch Press",
                "publication_year": 2022,
                "author": "Eric Matthes",
                "genre": "Programming",
                "cover_image": "python_crash_course.jpg"
            },
            {
                "title": "The Psychology of Money",
                "description": "Explores how emotions, behavior and personal experiences influence financial decisions and wealth management.",
                "isbn": "9780857197689",
                "publisher": "Harriman House",
                "publication_year": 2020,
                "author": "Morgan Housel",
                "genre": "Finance",
                "cover_image": "the_psychology_of_money.jpg"
            },
            {
                "title": "Sapiens",
                "description": "Explores the history of humankind, from early human societies to the development of modern civilization.",
                "isbn": None,
                "publisher": "Harper",
                "publication_year": 2015,
                "author": "Yuval Noah Harari",
                "genre": "History",
                "cover_image": "sapiens.jpg"
            },
            {
                "title": "The Midnight Library",
                "description": "Nora Seed discovers a mysterious library where each book represents a different life she could have lived.",
                "isbn": "9780525559474",
                "publisher": "Viking",
                "publication_year": 2020,
                "author": "Matt Haig",
                "genre": "Fiction",
                "cover_image": "the_midnight_library.jpg"
            }
        ]

        # -------------------------------
        # 5. INSERT BOOKS
        # -------------------------------

        added_books = 0

        for data in book_data:

            existing_book = db.query(Book).filter(
                Book.title == data["title"]
            ).first()

            if existing_book:
                continue

            book = Book(
                title=data["title"],
                description=data["description"],
                isbn=data["isbn"],
                publisher=data["publisher"],
                publication_year=data["publication_year"],
                author=authors[data["author"]],
                genre=genres[data["genre"]],
                cover_image=data["cover_image"],
                is_available=True
            )

            db.add(book)
            added_books += 1

        db.commit()

        print(f"{added_books} new books added successfully!")

        print("\nDatabase Summary:")
        print("Authors:", db.query(Author).count())
        print("Genres:", db.query(Genre).count())
        print("Books:", db.query(Book).count())

    except Exception as error:
        db.rollback()
        print("Error while inserting data:", error)

    finally:
        db.close()
        print("Database session closed.")


if __name__ == "__main__":
    seed_database()