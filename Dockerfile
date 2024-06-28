# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install chromium wget unzip -y

# Define the default command to run your application
CMD ["python", "main.py"]
