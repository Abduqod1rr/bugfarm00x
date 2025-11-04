# Base image
FROM python:3.12-slim

# Ishchi papka
WORKDIR /app

# Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App fayllarini ko‘chirish
COPY . .

# Portni expose qilish
EXPOSE 8000

# Run command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
