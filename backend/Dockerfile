# Base image - Python 3.12
FROM python:3.12-slim

# Set environment variables to optimize Python
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Create the app directory
RUN mkdir /app

# Set working directory
WORKDIR /app

# Upgrade pip
RUN pip install --upgrade pip

# Copy only requirements first to leverage Docker cache
# COPY pyproject.toml /app/
COPY requirements.txt /app/

# Install Python dependencies
# RUN pip install --no-cache-dir -e . # install via pyproject.toml
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application (development)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
