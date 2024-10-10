# Usar una imagen base de Python adecuada
FROM python:3.11-slim-buster

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos de requisitos y instalarlos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de tu aplicación
COPY . .

# Exponer el puerto en el que se ejecutará tu aplicación Flask
EXPOSE 8080

# Comando para ejecutar la aplicación cuando se inicie el contenedor
CMD ["python", "run.py"]