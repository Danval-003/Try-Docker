# Usa la imagen base de Python
FROM python:3.12.0

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos de la aplicación al contenedor
COPY . /app

# Instala las dependencias de la aplicación
RUN pip install --no-cache-dir -r requirements.txt

# Instala uWSGI
RUN pip install uwsgi

# Copia el archivo de configuración de uWSGI
COPY uwsgi.ini /app

# Copia el archivo de configuración de Nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Exponer el puerto 80 para que Nginx sea accesible desde fuera del contenedor
EXPOSE 80

# Ejecutar uWSGI con la configuración proporcionada
CMD ["uwsgi", "--ini", "uwsgi.ini"]
