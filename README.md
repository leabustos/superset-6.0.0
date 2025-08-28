Prueba de superset estable 6.0.0 en Docker para una baja concurrencia sin tener que recaer en K8s

PRUEBA 1:

- ir a ./old y ejecutar `docker compose up -d`

deberia levantar en `http:\\localhost:8088`

PRUEBA 2: 
Puse variables de entorno y trate de modularizar las cosas, haciendo que cada contenedor tenga una función como para empezar a trabajar con el esquema de microservicios.

Hasta ahora no me levantan los workers, por alguna razón intentan conectarse a una base de datos sqlite.
