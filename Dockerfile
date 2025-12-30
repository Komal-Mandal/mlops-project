# Use a supported Python image
FROM python:3.10-slim-bullseye

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port FastAPI will run on
EXPOSE 5000

# Command to run FastAPI
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
