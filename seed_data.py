from database import SessionLocal
from models import Author, Genre, Book


def seed_database():
    db = SessionLocal()

    try:
        # -----------------------------------------
        # 1. INSERT AND UPDATE AUTHORS
        # -----------------------------------------

        author_data = [
            {
                "name": "Héctor García and Francesc Miralles",
                "biography": "Authors known for exploring Japanese philosophy, lifestyle and personal development."
            },
            {
                "name": "Paulo Coelho",
                "biography": "Brazilian novelist known for philosophical and spiritual themes in his literary works."
            },
            {
                "name": "Khaled Hosseini",
                "biography": "Afghan-American novelist known for stories exploring friendship, family, love and Afghanistan."
            },
            {
                "name": "John Green",
                "biography": "American author known for contemporary young adult fiction and stories about life, friendship and relationships."
            },
            {
                "name": "Coltan Scrivner",
                "biography": "Behavioral scientist whose research explores morbid curiosity, human psychology and our attraction to frightening subjects."
            },
            {
                "name": "Hanya Yanagihara",
                "biography": "American novelist and editor known for emotionally complex literary fiction."
            },
            {
                "name": "Sam Bhagwat",
                "biography": "Technology entrepreneur and co-founder of Mastra, associated with the development of AI agent technologies."
            },
            {
                "name": "M. L. Rio",
                "biography": "American author known for literary fiction, Shakespearean themes and dark academia."
            },
            {
                "name": "James Clear",
                "biography": "Author and speaker known for research-based ideas about habits, behavior and personal improvement."
            },
            {
                "name": "Cal Newport",
                "biography": "Author and computer science professor known for his work on productivity, concentration and focused work."
            },
            {
                "name": "Robert C. Martin",
                "biography": "Software engineer and author known for software craftsmanship, clean coding principles and software architecture."
            },
            {
                "name": "Eric Matthes",
                "biography": "Programming educator and author known for creating practical learning resources for Python programming."
            },
            {
                "name": "Morgan Housel",
                "biography": "Financial writer and author known for explaining the relationship between psychology, money and financial decisions."
            },
            {
                "name": "Yuval Noah Harari",
                "biography": "Historian and author known for exploring human history, civilization and the development of human societies."
            },
            {
                "name": "Matt Haig",
                "biography": "British novelist and author known for contemporary fiction exploring human experiences, emotions and mental well-being."
            }
        ]

        for data in author_data:
            existing_author = db.query(Author).filter(
                Author.name == data["name"]
            ).first()

            if existing_author:
                existing_author.biography = data["biography"]
            else:
                db.add(Author(**data))

        db.commit()
        print("Authors added/updated successfully!")

        # -----------------------------------------
        # 2. INSERT AND UPDATE GENRES
        # -----------------------------------------

        genre_data = [
            {
                "name": "Self-help",
                "description": "Books focused on personal development, habits, motivation and self-improvement."
            },
            {
                "name": "Fiction",
                "description": "Imaginative stories featuring fictional characters, events and settings."
            },
            {
                "name": "Historical Fiction",
                "description": "Stories set in historical periods, combining fictional characters and events with historical settings."
            },
            {
                "name": "Young Adult",
                "description": "Literature primarily written for teenage and young adult readers, often exploring identity, friendship and growing up."
            },
            {
                "name": "Literary Fiction",
                "description": "Character-driven stories that explore human experiences, relationships and complex themes."
            },
            {
                "name": "Science",
                "description": "Books exploring scientific discoveries, research, human behavior and the natural world."
            },
            {
                "name": "Technology",
                "description": "Books about technological developments, computing, artificial intelligence and innovation."
            },
            {
                "name": "Mystery",
                "description": "Stories involving suspense, investigations, secrets and the discovery of hidden truths."
            },
            {
                "name": "Productivity",
                "description": "Books about time management, concentration, effective work habits and personal efficiency."
            },
            {
                "name": "Programming",
                "description": "Books that teach programming languages, software development techniques and coding principles."
            },
            {
                "name": "Finance",
                "description": "Books exploring money management, investing, financial decisions and financial behavior."
            },
            {
                "name": "History",
                "description": "Books exploring past events, historical figures, civilizations and the development of human societies."
            }
        ]

        for data in genre_data:
            existing_genre = db.query(Genre).filter(
                Genre.name == data["name"]
            ).first()

            if existing_genre:
                existing_genre.description = data["description"]
            else:
                db.add(Genre(**data))

        db.commit()
        print("Genres added/updated successfully!")

        # -----------------------------------------
        # 3. RETRIEVE AUTHORS AND GENRES
        # -----------------------------------------

        authors = {
            author.name: author
            for author in db.query(Author).all()
        }

        genres = {
            genre.name: genre
            for genre in db.query(Genre).all()
        }

        # -----------------------------------------
        # 4. BOOK DATA
        # -----------------------------------------

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

        # -----------------------------------------
        # 5. INSERT BOOKS
        # -----------------------------------------

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

        # -----------------------------------------
        # 6. DATABASE SUMMARY
        # -----------------------------------------

        print("\nDatabase Summary:")
        print("Authors:", db.query(Author).count())
        print("Genres:", db.query(Genre).count())
        print("Books:", db.query(Book).count())

        # Check for missing biographies
        missing_biographies = db.query(Author).filter(
            Author.biography.is_(None)
        ).count()

        # Check for missing genre descriptions
        missing_descriptions = db.query(Genre).filter(
            Genre.description.is_(None)
        ).count()

        print("\nData Verification:")
        print("Authors without biographies:", missing_biographies)
        print("Genres without descriptions:", missing_descriptions)

    except Exception as error:
        db.rollback()
        print("Error while inserting data:", error)

    finally:
        db.close()
        print("Database session closed.")


if __name__ == "__main__":
    seed_database()