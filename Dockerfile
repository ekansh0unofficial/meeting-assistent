FROM python:3.11-slim

# Install system dependencies for ML/AI packages
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    git \
    libasound2-dev \
    libffi-dev \
    libsndfile1 \
    ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first and install them
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip && \
    pip install --default-timeout=100 --retries 10 --no-cache-dir -r requirements.txt

# 🔽 NLTK Resource Fix: Download 'stopwords'
RUN python -m nltk.downloader -d /usr/local/nltk_data stopwords

# Copy the rest of the code
COPY . .

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

# Set environment variable so NLTK can find the data
ENV NLTK_DATA=/usr/local/nltk_data

# Expose app port
EXPOSE 8000

# Launch the app using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
