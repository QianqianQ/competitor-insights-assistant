# Stage 1: Base build stage
FROM python:3.12-slim AS builder

# Set environment variables to optimize Python
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Create the app directory
RUN mkdir /app

# Set the working directory
WORKDIR /app

# Upgrade pip
RUN pip install --upgrade --root-user-action=ignore pip

# Copy the requirements file first (better caching)
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir --root-user-action=ignore -r requirements.txt

# Stage 2: Production stage
FROM python:3.12-slim

RUN useradd -m -r appuser && \
   mkdir /app && \
   mkdir -p /app/static && \
   mkdir -p /app/media && \
   chown -R appuser:appuser /app

# Copy the Python dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Set the working directory
WORKDIR /app

# Copy application code
COPY --chown=appuser:appuser . .

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Switch to non-root user
USER appuser

RUN chmod +x docker-entrypoint.sh

# Collect static files during build
RUN python manage.py collectstatic --noinput

# Expose the application port
EXPOSE 8000

# Start the application using Gunicorn
ENTRYPOINT ["./docker-entrypoint.sh"]
