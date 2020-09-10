import json
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, unique=True)
    todos = db.Column(db.String, nullable=False)
    
    def serialize(self):
        return json.loads(self.todos)

    def serialize_all_data(self):
        return {
            "id": self.id,
            "username": self.username,
            "todos": self.todos
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):       
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()