# Use the official Node.js image as a base
FROM node:22-alpine

# Set the working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy app files
COPY . .

# Expose the port the app runs on
EXPOSE 3000

# Run the app (hot-reload)
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
