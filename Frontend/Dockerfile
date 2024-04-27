# Use Node.js as a base image
FROM node:20

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json package-lock.json /app/

# Install dependencies
RUN npm install

COPY . /app

# Make port 3000 available to the outside this container
EXPOSE 3000

# Command to run your app
CMD ["npm", "start"]
