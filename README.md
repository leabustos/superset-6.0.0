Prueba de superset estable 6.0.0 en Docker para una baja concurrencia sin tener que recaer en K8s

PRUEBA 1:

- ir a ./old y ejecutar `docker compose up -d`

deberia levantar en `http:\\localhost:8088`

PRUEBA 2: 
Puse variables de entorno y trate de modularizar las cosas, haciendo que cada contenedor tenga una función como para empezar a trabajar con el esquema de microservicios.

Hasta ahora no me levantan los workers, por alguna razón intentan conectarse a una base de datos sqlite.

para levantar el proyecto recorda crear un `.env` basado en el `.env.example` y completar las variables de entorno con una clave con `openssl rand -base64 42`

Trate de configurar los webservers para que puedan operar con perfiles de **http** y **ssl**.
luego ejecutar:
```bash
docker compose --profile http up -d
```
En el caso de que tengamos certificados podemos ponerlos en la carpeta `./certs` y luego ejecutar:
 ```bash
docker compose --profile ssl up -d
```
