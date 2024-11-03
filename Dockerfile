# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /mutante_parcialds

# Copia los archivos de la aplicación al contenedor
COPY . /mutant_app

# Instala las dependencias desde requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto en el que correrá la aplicación (por ejemplo, 8000 si usas Uvicorn)
EXPOSE 8000

# Especifica la variable de entorno para que Python no almacene archivos .pyc
ENV PYTHONUNBUFFERED=1

# Comando de inicio para ejecutar main.py
CMD ["python", "main.py"]