FROM python:3.10-slim-bullseye

WORKDIR /app

# Copy everything first, so pyproject.toml is available
COPY . .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
