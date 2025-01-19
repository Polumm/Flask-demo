from app import create_app
from app.models import db, Upload
from app.config import TestConfig


# Create the Flask app with TestConfig
app = create_app()
app.config.from_object(TestConfig)
client = app.test_client()  # Create a test client


def setUpModule():
    """
    Set up the test environment before running any tests.
    """
    with app.app_context():
        db.create_all()  # Create all tables


def tearDownModule():
    """
    Clean up the test environment after all tests have run.
    """
    with app.app_context():
        db.session.remove()
        db.drop_all()


# Helper function to populate the database
def populate_database():
    with app.app_context():
        for i in range(5):  # Add 5 image entries
            upload = Upload(text=f"Image {i}", image_data=b"test_data")
            db.session.add(upload)
        db.session.commit()


# Helper function to clear the database
def clear_database():
    with app.app_context():
        db.session.query(Upload).delete()
        db.session.commit()


def test_random_images():
    """
    Test the API with a valid number of requested images.
    """
    populate_database()
    response = client.get("/api/image/random/3")
    assert response.status_code == 200

    data = response.get_json()
    assert len(data) == 3
    for item in data:
        assert "id" in item
        assert "image_url" in item

    clear_database()


def test_random_images_more_than_available():
    """
    Test the API when requesting more images than available in the database.
    """
    populate_database()
    response = client.get("/api/image/random/10")
    assert response.status_code == 200

    data = response.get_json()
    assert len(data) == 5  # Only 5 images exist in the database

    clear_database()


def test_random_images_zero():
    """
    Test the API with a request for 0 images.
    """
    populate_database()
    response = client.get("/api/image/random/0")
    assert response.status_code == 200

    data = response.get_json()
    assert len(data) == 0  # No images should be returned

    clear_database()


def test_no_images_in_database():
    """
    Test the API when the database is empty.
    """
    clear_database()  # Ensure database is empty
    response = client.get("/api/image/random/3")
    assert response.status_code == 404

    data = response.get_json()
    assert data["message"] == "No images available."
