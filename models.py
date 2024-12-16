from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ImageModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_filename = db.Column(db.String(100))
    resized_filename = db.Column(db.String(100))
    original_path = db.Column(db.String(200))
    resized_path = db.Column(db.String(200))
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
