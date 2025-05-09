# Use an official Python base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy only requirements to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the whole project into the container
COPY . .

# Give execution permission to the start script
RUN chmod +x start.sh

# Expose FastAPI default port
EXPOSE 8000

# Start the application using the shell script
CMD ["./start.sh"]
