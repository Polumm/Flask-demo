import random
from flask import Blueprint, jsonify, render_template, current_app
from .models import Upload
from .api import UploadAPI

routes = Blueprint("routes", __name__)


@routes.route("/api/image/<int:upload_id>")
def get_image(upload_id):
    upload = Upload.query.get(upload_id)
    if not upload:
        return {"message": "Image not found"}, 404

    return current_app.response_class(upload.image_data, mimetype="image/jpeg")


@routes.route("/api/image/random/<int:num>")
def get_random_image(num):
    uploads = Upload.query.with_entities(Upload.id, Upload.text).all()
        # Check if there are enough images
    if not uploads:
        return jsonify({"message": "No images available."}), 404
    
    # Get the minimum between requested number and available images
    num_to_fetch = min(num, len(uploads))
    
    # Randomly select the images
    random_images = random.sample(uploads, num_to_fetch)
    
    # Build the response with image URLs
    result = [
        {"id": image.id, "image_url": f"/api/image/{image.id}"}
        for image in random_images
    ]
    
    return jsonify(result), 200
    
@routes.route("/")
def index():
    # Call UploadAPI.get() to get the uploads data
    uploads_api = UploadAPI()
    uploads_data, status_code = (
        uploads_api.get()
    )  # get() returns (data, status_code)

    if status_code != 200:
        return jsonify({"error": "Failed to fetch uploads"}), status_code

    # Render the uploads data in the template
    return render_template("index.html", uploads=uploads_data)
