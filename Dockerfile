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
COPY .  .

# Expose the application port
EXPOSE 8000

# Run the tests and then start the application
CMD ["sh", "-c", "pytest tests && flask run --host=0.0.0.0 --port=8000"]
