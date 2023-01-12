from main import db
from datetime import datetime


class Notes(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.String(1000))
    body = db.Column(db.String(10000))
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    archive = db.Column(db.Boolean, default=0)
    edit_date = db.Column(db.DateTime)

    def __repr__(self):
        return '<Notes %r>' % self.note_id

    def __init__(self, header, body):
        self.header = header
        self.body = body
