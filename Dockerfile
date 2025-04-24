# Usa una imagen oficial de Python como base
FROM python:3.10-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos necesarios
COPY . /app

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto en el que tu app corre
EXPOSE 8080

# Comando para ejecutar la app con Gunicorn
CMD ["gunicorn", "servidor:app", "--bind", "0.0.0.0:8080"]

