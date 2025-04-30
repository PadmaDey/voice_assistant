# # Use Python 3.9 slim image
# FROM python:3.9-slim

# # Set environment variables
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# # Install system dependencies
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     ffmpeg \
#     git \
#     libglib2.0-0 \
#     libsm6 \
#     libxrender1 \
#     libxext6 \
#     && rm -rf /var/lib/apt/lists/*

# # Set working directory
# WORKDIR /app

# # Copy requirements and install dependencies
# COPY requirements.txt .
# RUN pip install --upgrade pip && \
#     pip install --no-cache-dir -r requirements.txt

# # Copy the rest of the app
# COPY . .

# # Expose port (FastAPI/Flask)
# EXPOSE 8000

# # Use Gunicorn with Uvicorn worker for FastAPI or Flask
# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]








# Use official Python image
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Copy all project files to the container
COPY . .

# Install system-level dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose the Flask app port
EXPOSE 5000

# Start the Flask app
CMD ["python", "app.py"]
