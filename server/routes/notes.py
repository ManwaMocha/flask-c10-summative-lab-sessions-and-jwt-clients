from flask import Blueprint, jsonify, request, session
from config import db
from models import Note
from routes.security import login_required, owned_note, pagination_options

#Groups all Notes-related routes together
notes_bp = Blueprint('notes', __name__)

#Get all notes
@notes_bp.get('/notes')
@login_required
def get_notes():
    options = pagination_options(request.args)

    if options is None:
        return jsonify({'error': 'Use page >= 1 and per_page between 1 and 100'}), 400

        page, per_page = options

        #Get only the logged-in user's notes
        query = Note.query.filter_by(user_id=session['user_id']).order_by(Note.id.asc())

        result = db.paginate (query, page=page, per_page=per_page, error_out=False)

        return jsonify({
            'notes': [note.to_dict() for note in result.items],
            'page': page,
            'per_page': per_page,
            'total': result.total,
            'pages': result.page
        }), 200



