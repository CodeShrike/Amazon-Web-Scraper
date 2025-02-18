# Dockerfile for app
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy app files
COPY . .

# Install dependencies in the correct order
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask port
EXPOSE 5000

# Command to run the app
CMD ["python", "run.py"]
