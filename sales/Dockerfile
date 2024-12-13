# Use the official Python image as a base image
FROM python:3.11-slim

# Set environment variables to prevent Python from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set a working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . /app/

# Expose the application port
EXPOSE 5004

# Run the application
CMD ["python", "app.py"]
