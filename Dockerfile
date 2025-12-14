# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    FLASK_APP=pomodoro.py

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY pomodoro.py .
COPY templates/ templates/

# Create directory for data persistence
RUN mkdir -p /data

# Expose port 5000
EXPOSE 5000

# Run the application
CMD ["python3", "pomodoro.py"]
