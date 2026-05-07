from extensions import db
from datetime import datetime

class Log(db.Model):
    __tablename__ = 'logs'
    id        = db.Column(db.Integer, primary_key=True)
    username  = db.Column(db.String(80), nullable=False)
    action    = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Log {self.username} - {self.action}>'
