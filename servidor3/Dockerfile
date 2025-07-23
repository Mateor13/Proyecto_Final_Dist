FROM python:3.9-slim

WORKDIR /app

# Copiar requirements.txt desde la carpeta servidor3
COPY servidor3/requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar archivos de la aplicación desde servidor3
COPY servidor3/ .

EXPOSE 3000
CMD ["python", "app.py"]