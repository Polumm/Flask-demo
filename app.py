import os
from flask import Flask, request, render_template
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database credentials from .env file
DB_URL = os.getenv("DB_URL")
DB_USER = os.getenv("DB_USERNAME")
DB_PASS = os.getenv("DB_PASSWORD")

# Optional: Test DB credentials for testing environments
TEST_DB_URL = os.getenv("TEST_DB_URL")
TEST_DB_USER = os.getenv("TEST_DB_USERNAME")
TEST_DB_PASS = os.getenv("TEST_DB_PASSWORD")

if not DB_URL or not DB_USER or not DB_PASS:
    raise RuntimeError("Missing DB credentials. Check your .env file.")

# Initialize Flask app
app = Flask(__name__)

# Set up database URI
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL  # Use main database
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Set upload folder for storing images
app.config["UPLOAD_FOLDER"] = "./static/uploaded_images"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Initialize Flask-Restful API and SQLAlchemy database
api = Api(app)
db = SQLAlchemy(app)


# Database model for storing text and image information
class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    image_data = db.Column(
        db.LargeBinary, nullable=False
    )  # Store binary image data


# RESTful API resource for uploading and retrieving data
class UploadAPI(Resource):
    def post(self):
        """
        Handle POST request to upload text and image.
        """
        text = request.form.get("text")
        image = request.files.get("image")

        if not text or not image:
            return {"message": "Text and image are required"}, 400

        # Read the image file as binary data
        image_data = image.read()

        # Save the text and image data to the database
        upload_entry = Upload(text=text, image_data=image_data)
        db.session.add(upload_entry)
        db.session.commit()

        return {"message": "Upload successful", "id": upload_entry.id}, 201

    def get(self):
        """
        Retrieve all uploaded content from the database.
        """
        uploads = Upload.query.all()
        result = [
            {
                "id": upload.id,
                "text": upload.text,
                "image_url": f"/api/image/{upload.id}",  # URL to fetch the image
            }
            for upload in uploads
        ]
        return result, 200


# Add the RESTful API endpoint
api.add_resource(UploadAPI, "/api/upload")


# Serve image data dynamically
@app.route("/api/image/<int:upload_id>")
def get_image(upload_id):
    """
    Fetch the image data from the database and serve it.
    """
    upload = Upload.query.get(upload_id)
    if not upload:
        return {"message": "Image not found"}, 404

    return app.response_class(
        upload.image_data, mimetype="image/jpeg"
    )  # Set appropriate MIME type


# Route for rendering the uploaded content
@app.route("/")
def index():
    uploads = Upload.query.all()
    processed_data = [
        {"text": upload.text.upper(), "image_url": f"/api/image/{upload.id}"}
        for upload in uploads
    ]
    return render_template("index.html", uploads=processed_data)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
