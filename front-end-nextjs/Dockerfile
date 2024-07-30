# Use the official Node.js image from the Docker Hub

FROM node:16-alpine

# Set the working directory in the container

WORKDIR /app

# Copy the package.json and package-lock.json files

COPY frontend/package*.json ./

# Install the dependencies

RUN npm install

# Copy the rest of the application code into the container

COPY frontend/ .

# Build the Next.js application

RUN npm run build

# Expose port 3000 to the outside world

EXPOSE 3000

# Command to run the Next.js server

CMD ["npm", "start"]

