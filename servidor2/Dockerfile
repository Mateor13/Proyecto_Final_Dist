FROM python:3.9-slim

WORKDIR /app

# Copiar requirements.txt desde la carpeta servidor2
COPY servidor2/requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar archivos de la aplicación desde servidor2
COPY servidor2/ .

EXPOSE 3000
CMD ["python", "app.py"]