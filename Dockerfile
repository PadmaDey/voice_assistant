# Use official Python image
# FROM python:3.9-slim
FROM python:3.9-alpine

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

# ✅ Explicitly set PORT env var    
ENV PORT=5000  

# Expose the Flask app port
EXPOSE 5000

# Start the Flask app
CMD ["python", "app.py"]
