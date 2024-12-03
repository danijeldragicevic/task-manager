# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Prevent Python from writing .pyc files to __pycache__ directory to save disk space.
ENV PYTHONDONTWRITEBYTECODE 1

# Ensure that the standard output and error streams are unbuffered.
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file and install the dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code into the container
COPY .  /app/

# Expose the application port
EXPOSE 8000

# Command to run the application
CMD ["python", "app/main.py"]
