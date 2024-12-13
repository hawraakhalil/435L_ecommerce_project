# Use the official Python image as the base
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire admin directory into the container
COPY . .

# Add /app to the PYTHONPATH to recognize src as a module
ENV PYTHONPATH=/app

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV SQLALCHEMY_DATABASE_URI=sqlite:////app/data/admin.db
ENV SQLALCHEMY_TRACK_MODIFICATIONS=False

# Expose the port Flask will run on
EXPOSE 5000

# Run database migrations
RUN flask db upgrade || true

# Start the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
