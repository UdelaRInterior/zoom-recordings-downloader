# Zoom Recordings Downloader

> Este [README en inglés](README.md)

Una librería Python para descargar las grabaciones de cuentas Zoom.us

## Arquitectura y requisitos

Para poder descargar las grabaciones utilizando este utilitaro, se debe disponer de una cuenta Zoom con privilegios developer en la nube Zoom. Se podrá entonces descargar las grabaciones de todas las salas Zoom a las que la cuenta utilizada tenga acceso. 

La librería es llamada desde un programa que corre en un servidor o sistema local capaz de ejecutar Python, y accede a los recursos de la nube Zoom a través de una [API JWT](https://marketplace.zoom.us/docs/guides/auth/jwt).


## Dependencias en el sistema local

* Python versión 3.6 o superior
* Además, se debe instalar los siguientes paquetes:
   * zoomus
   * python-decouple
   * python-dateutil

En sistemas Debian o derivados, se puede instalar las dependencias necesarias así:
```
apt install python3-venv python3-pip
pip3 install zoomus
pip3 install python-decouple
pip3 install python-dateutil
```

## Uso

Primero deberá crear una JWT App accediendo con las credenciales de su cuenta en el [Marketplace de Zoom](https://marketplace.zoom.us/) para lo cual se recomiendoa seguir [esta documentación](https://marketplace.zoom.us/docs/guides/build/jwt-app).

Luego de esto deberá crear un archivo denominado `.env` (archivo oculto a `ls`) dentro del mismo directorio donde ubique la librería `zoom_recordings.py`. Puede tomar como referencia el ejemplo [`example.env`](example.env). `.env` es el archivo de configuración de la librería. Allí deberá indicar entre otras cosas:
* las credenciales (`API_KEY` y `API_SECRET`) de su JWT App recientemente creada.
* la fecha incial (`start_year`, `start_month`, `start_day_of_month`) a partir de la cual se quieren seleccionar las grabaciones (por su fecha de grabación).
* rutas de directorios para ubicar las grabaciones descargadas (`download_root_path`) y los logs (`log_dir_path`).

Por último, para usar la librería `zoom_recordings.py`, puede crear otro archivo .py donde importar la funcion `download_recordings` y personalizar su invocación. Esta función recibe por parámetro la lista de usuarios (`users_selected`) para los cuales se desean descargar sus grabaciones. A continuación un ejemplo de su utilización:

```
from zoom_recordings import download_recordings

users_selected=["user01@example.com","user02@example.com"]
download_recordings(users_selected)
```
Y luego corre ese script con python 3. Digamos que el archivo con el precedente código se llama `descargar_misgrabaciones.py` y que estamos en un host debian: 
```
$ python3 descargar_misgrabaciones.py
```
Puede encontrar otro ejemplo en [`example_main.py`](example_main.py).
