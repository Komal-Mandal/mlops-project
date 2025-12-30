# Use an official Python 3.10 image
FROM python:3.10-slim-buster

# Set working directory
WORKDIR /app

# Upgrade pip first
RUN pip install --upgrade pip

# Copy requirements first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Install your local package in editable mode (if you have src/ as in your logs)
RUN pip install --no-cache-dir -e ./src

# Expose the port FastAPI will run on
EXPOSE 5000

# Add a non-root user for safety
RUN useradd -m appuser
USER appuser

# Command to run FastAPI
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
