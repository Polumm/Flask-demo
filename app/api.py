from flask_restful import Resource
from flask import request, redirect, url_for
from .models import Upload, db


class UploadAPI(Resource):
    def post(self):
        text = request.form.get("text")
        image = request.files.get("image")

        if not text or not image:
            return {"message": "Text and image are required"}, 400

        image_data = image.read()
        upload_entry = Upload(text=text, image_data=image_data)
        db.session.add(upload_entry)
        db.session.commit()

        # return {"message": "Upload successful", "id": upload_entry.id}, 201
        # Redirect to home after successful upload
        return redirect(url_for("routes.index"))

    def get(self):
        uploads = Upload.query.with_entities(Upload.id, Upload.text).all()
        result = [
            {
                "id": upload.id,
                "text": upload.text,
                "image_url": f"/api/image/{upload.id}",
            }
            for upload in uploads
        ]
        return result, 200
