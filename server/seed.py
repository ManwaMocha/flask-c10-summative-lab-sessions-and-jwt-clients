
from app import app
from config import db
from models import User, Note, Category


def seed_data():
    with app.app_context():

        # SAMPLE USERS
        users_data = [
            {
                "username": "john",
                "password": "password123"
            },
            {
                "username": "mary",
                "password": "password456"
            }
        ]

        users = {}

        # Create users if they don't already exist
        for user_data in users_data:
            user = User.query.filter_by(
                username=user_data["username"]
            ).first()

            if not user:
                user = User(username=user_data["username"])
                user.set_password(user_data["password"])
                db.session.add(user)
                db.session.flush()

            users[user.username] = user

        # SAMPLE CATEGORIES
        categories_data = ["School", "Personal", "Work"]

        categories = {}

        # Create categories if they don't already exist
        for category_name in categories_data:
            category = Category.query.filter_by(
                name=category_name
            ).first()

            if not category:
                category = Category(name=category_name)
                db.session.add(category)
                db.session.flush()

            categories[category_name] = category

        # SAMPLE NOTES
        notes_data = [
            {
                "title": "My First Note",
                "content": "This is John's first sample note.",
                "username": "john",
                "category": "School"
            },
            {
                "title": "Learning Flask",
                "content": "I am learning how to build APIs with Flask.",
                "username": "john",
                "category": "School"
            },
            {
                "title": "My Daily Tasks",
                "content": "Complete assignments and practise coding.",
                "username": "mary",
                "category": "Personal"
            },
            {
                "title": "Project Ideas",
                "content": "Build useful applications using Python.",
                "username": "mary",
                "category": "Work"
            }
        ]

        # Create notes without duplicating existing ones
        for note_data in notes_data:
            user = users[note_data["username"]]
            category = categories[note_data["category"]]

            existing_note = Note.query.filter_by(
                title=note_data["title"],
                user_id=user.id
            ).first()

            if not existing_note:
                note = Note(
                    title=note_data["title"],
                    content=note_data["content"],
                    user_id=user.id,
                    category_id=category.id
                )
                db.session.add(note)

            # Connect existing sample notes to their categories
            elif existing_note.category_id is None:
                existing_note.category_id = category.id

        db.session.commit()

        print("Sample users, categories and notes seeded successfully!")


if __name__ == "__main__":
    seed_data()
