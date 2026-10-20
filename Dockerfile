# Use the official Python image
FROM python:3.10-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project
COPY . .

# Collect static assets
RUN python manage.py collectstatic --noinput

# Expose the application port
EXPOSE 8000

# Apply migrations, then start Gunicorn
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn voi_start.wsgi:application --bind 0.0.0.0:8000 --timeout 180"]