# Use a slim Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy files into the container
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port 5000 (Flask default)
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
