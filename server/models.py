
from config import db, bcrypt


# USER MODEL
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    # One user can have many notes
    notes = db.relationship(
        'Note',
        back_populates='user',
        cascade='all, delete-orphan'
    )

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(
            password
        ).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(
            self.password_hash, password
        )

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username
        }


# NOTE MODEL
class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)

    # Foreign key connecting Note to User
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    # Foreign key connecting Note to Category
    # Nullable so existing notes can have no category
    category_id = db.Column(
        db.Integer,
        db.ForeignKey('categories.id'),
        nullable=True
    )

    # Many notes can belong to one user
    user = db.relationship(
        'User',
        back_populates='notes'
    )

    # Many notes can belong to one category
    category = db.relationship(
        'Category',
        back_populates='notes'
    )

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'user_id': self.user_id,
            'category_id': self.category_id
        }


# CATEGORY MODEL
class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    # One category can contain many notes
    notes = db.relationship(
        'Note',
        back_populates='category'
    )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
