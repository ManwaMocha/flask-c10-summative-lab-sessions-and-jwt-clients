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

    result = db.paginate(query, page=page, per_page=per_page, error_out=False)

    return jsonify({
            'notes': [note.to_dict() for note in result.items],
            'page': page,
            'per_page': per_page,
            'total': result.total,
            'pages': result.pages
        }), 200

#Get one note
@notes_bp.get('/notes/<int:note_id>')
@login_required
def get_note(note_id):
    note = owned_note(note_id)

    if note is None:
        return jsonify({'error': 'Note not found'}), 404

    return jsonify(note.to_dict()), 200

#Create a new note
@notes_bp.post('/notes')
@login_required
def create_note():
    data = request.get_json(silent=True) or {} 

    title = data.get('title')
    content = data.get('content')

    if not isinstance(title, str) or not title.strip() or len(title.strip()) > 150:
        return jsonify({'error': 'Title must be 1-150 characters'}), 400

    if not isinstance(content, str) or not content.strip():
        return jsonify({'error': 'Content is required'}), 400

    note = Note(
        title=title.strip(),
        content=content.strip(),
        user_id=session['user_id']
    )

    db.session.add(note)
    db.session.commit()

    return jsonify(note.to_dict()), 201

#Update an existing note
@notes_bp.patch('/notes/<int:note_id>')
@login_required
def update_note(note_id):
    note = owned_note(note_id)

    if note is None:
        return jsonify({'error': 'Note not found'}), 404

    data = request.get_json(silent=True) or {}

    if 'title' not in data and 'content' not in data:
        return jsonify({'error': 'Provide a title or content to update'}), 400

    if 'title' in data:
        title = data['title']
        if not isinstance(title, str) or not title.strip() or len(title.strip()) > 150:
            return jsonify({'error': 'Title must be 1-150 characters'}), 400
        note.title = title.strip()

    if 'content' in data:
        content = data['content']
        if not isinstance(content, str) or not content.strip():
            return jsonify({'error': 'Content is required'}), 400
        note.content = content.strip()

    db.session.commit()

    return jsonify(note.to_dict()), 200

#Delete a note
@notes_bp.delete('/notes/<int:note_id>')
@login_required
def delete_note(note_id):
    note = owned_note(note_id)

    if note is None:
        return jsonify({'error': 'Note not found'}), 404

    db.session.delete(note)
    db.session.commit()

    return '', 204






