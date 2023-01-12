from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_restful import fields, marshal_with
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/testAPI.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

notesFields = {
    'id': fields.Integer,
    'header': fields.String,
    'body': fields.String,
    'create_date': fields.DateTime,
    'archive': fields.Boolean,
    'edit_date': fields.DateTime
}


@app.route('/api/notes', methods=['GET'])
@marshal_with(notesFields)
def get_notes():
    notes = db.session.query(Notes).all()
    return notes


@app.route('/api/note/<int:id>', methods=['GET'])
@marshal_with(notesFields)
def get_note(id):
    note = db.session.query(Notes).get_or_404(id)
    return note


@app.route('/api/note/create', methods=['POST'])
def create_note():
    header = request.json['header']
    body = request.json['body']
    note = Notes(header, body)

    db.session.add(note)
    db.session.commit()
    return 'Successful operation'


@app.route('/api/note/<int:id>/archive', methods=['POST'])
def archive_note(id):
    note = db.session.query(Notes).get_or_404(id)
    note.archive = 1
    db.session.add(note)
    db.session.commit()
    return 'Successful operation'


@app.route('/api/note/<int:id>/archive/return', methods=['POST'])
def archive_note_return(id):
    note = db.session.query(Notes).get_or_404(id)
    note.archive = 0
    db.session.add(note)
    db.session.commit()
    return 'Successful operation'


@app.route('/api/note/<int:id>/edit', methods=['POST'])
def edit_note(id):
    note = db.session.query(Notes).get_or_404(id)
    note.header = request.json['header']
    note.body = request.json['body']
    if note.archive == 1:
        return 'archive note', 500
    else:
        db.session.add(note)
        db.session.commit()
    return 'Successful operation'


@app.route('/api/note/<int:id>/delete', methods=['DELETE'])
def delete_note(id):
    note = db.session.query(Notes).get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    return 'Successful operation'


@app.errorhandler(404)
def not_found(error):
    if request.path.startswith('/api/note/'):
        return 'Note does not exist', 404
    else:
        return 'Not exist', 404


if __name__ == '__main__':
    app.run(debug=True)
