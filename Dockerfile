# # 1. Base Image
# FROM python:3.12.7-slim

# # 2. Set environment variables
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# # 3. Set work directory
# WORKDIR /app

# # 4. Install dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir --upgrade pip \
#     && pip install --no-cache-dir -r requirements.txt

# # 5. Copy project files
# COPY . .

# # 6. Expose port (Render expects your app to be listening)
# EXPOSE 5000

# # 7. Run the app using gunicorn (recommended for production)
# CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]






# # Use official lightweight Python 3.12 image
# FROM python:3.12-slim

# # Set working directory
# WORKDIR /app

# # Install basic dependencies
# RUN apt-get update && apt-get install -y \
#     ffmpeg \
#     libsndfile1 \
#     && rm -rf /var/lib/apt/lists/*

# # Copy requirements (you should create a requirements.txt separately)
# COPY requirements.txt .

# # Install Python dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the rest of the application code
# COPY . .

# # Expose port (Render uses $PORT env variable)
# EXPOSE 5000

# # Run the app
# CMD ["python", "app.py"]





# Use official slim Python 3.12 image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    make \
    ffmpeg \
    libsndfile1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Run app
CMD ["python", "app.py"]
