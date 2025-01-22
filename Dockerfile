# Use an official Python runtime as the base image
FROM python:3.12.4

# Set the working directory in the container
WORKDIR /app

# Copy the application code to the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the Flask app runs on
EXPOSE 5001

# Define the command to run the Flask app
CMD ["python", "app.py"]
