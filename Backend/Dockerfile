FROM python:3.11.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code to the container
COPY src/ /app/

# Copy the start-up script and ensure it is executable
COPY src/start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run start.sh when the container launches
CMD ["python", "populate.py"]

CMD ["python", "endpoints.py"]
