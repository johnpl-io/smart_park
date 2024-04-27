# Use Node.js as a base image
FROM node:20

# Set the working directory in the container
WORKDIR /app

# Copy the proxy server files
COPY gmap.js /app

# Install Express or any other dependencies you need
RUN npm install express
RUN npm install cors

# Make port 2000 available to the outside this container
EXPOSE 2000

# Command to run the proxy server
CMD ["node", "gmap.js"]
