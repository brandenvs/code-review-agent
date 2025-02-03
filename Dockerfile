# syntax=docker/dockerfile:1
FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    g++ \
    python3-dev \
    git \
    libgl1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements first to cache dependencies
COPY requirements.txt .
RUN python3 -m venv /app/venv \
    && /app/venv/bin/pip install --upgrade pip setuptools wheel \
    && /app/venv/bin/pip install -r requirements.txt

# Update PATH for the virtual environment
ENV PATH="/app/venv/bin:$PATH"

# Copy application code
COPY videoAPI/ /app/videoAPI/
COPY .env /app/.env

# Default command
CMD ["python", "-m", "videoAPI"]
