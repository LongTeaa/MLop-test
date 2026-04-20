FROM python:3.9-slim

WORKDIR /app

# Copy requirement files first for layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY . .

# Explicitly ensure models directory exists and model is there
RUN mkdir -p models

EXPOSE 5000

# Start Flask app using gunicorn for production quality
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]