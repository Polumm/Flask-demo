from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    image_data = db.Column(
        db.LargeBinary, nullable=False
    )  # Store binary image data
