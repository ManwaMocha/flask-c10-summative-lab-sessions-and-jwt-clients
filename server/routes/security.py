from functools import wraps
from flask import jsonify, session
from models import Note


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "Unauthorized"}), 401

        return func(*args, **kwargs)

    return wrapper



def owned_note(note_id):
    user_id = session.get("user_id")

    note = Note.query.filter_by(
        id=note_id,
        user_id=user_id
    ).first()

    return note

def pagination_options(args):
    try:
        page = int(args.get("page", 1))#query parameter value arrive as stringd
        per_page = int(args.get("per_page", 10))
    except (ValueError, TypeError):
        return None

    if page < 1 or per_page < 1 or per_page > 100:
        return None

    return page, per_page
