# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY api/requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container

COPY api/ .

# Command to run the FastAPI server

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

