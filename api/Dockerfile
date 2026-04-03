# Pull python image
FROM python:3.9

# Set working dir in the container
WORKDIR /usr/src/app

# Copy dependencies file to the working directory in the container
COPY requirements.txt ./

# Install all the packages needed (that are in the requirements.txt)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src dir to the working directory in the container
COPY . .

# Run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]