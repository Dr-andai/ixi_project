# Use slim Python image for smaller size
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev gcc build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Expose port
EXPOSE 10000

# Start the app (Render overrides port via $PORT)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
