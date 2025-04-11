# Usa una imagen base de Python
FROM python:3.11

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del proyecto
COPY . .

# Expone el puerto 8000
EXPOSE 8000

# Comando por defecto (lo puede sobrescribir docker-compose)
CMD ["python", "./manage.py", "runserver", "0.0.0.0:8000"]
