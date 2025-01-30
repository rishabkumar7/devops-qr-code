# Use the official lightweight Node.js 18 image
FROM node:18-alpine AS base

# Set the working directory in the container
WORKDIR /app

# Copy the package files
COPY package.json yarn.lock* package-lock.json* pnpm-lock.yaml* ./

# Copy the install-dependencies.sh script
COPY install-dependencies.sh ./

# Install dependencies using the script
RUN chmod +x ./install-dependencies.sh && ./install-dependencies.sh

# Copy the rest of the application code
COPY . .

# Run the Next.js build step
RUN npm run build

# Expose the build folder
RUN mkdir -p .next

# Copy the .next folder (to avoid context issues)
COPY .next ./.next

# Expose the application port
EXPOSE 3000

# Start the application
CMD ["npm", "start"]
