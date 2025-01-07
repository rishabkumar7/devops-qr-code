# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /usr/src/app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the API code into the container
COPY . .

# Expose the API server port
EXPOSE 8000

# Set the environment variable for AWS keys (optional for .env)
ENV ENV_FILE_PATH=.env

# Start the API server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
