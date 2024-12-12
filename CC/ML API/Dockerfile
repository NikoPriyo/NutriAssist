# Gunakan Python sebagai base image
FROM python:3.9-slim

# Tetapkan direktori kerja
WORKDIR /app

# Salin semua file ke dalam container
COPY . .

# Install dependensi
RUN pip install --no-cache-dir -r requirements.txt

# Expose port untuk FastAPI
EXPOSE 8080

# Jalankan aplikasi FastAPI menggunakan Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
