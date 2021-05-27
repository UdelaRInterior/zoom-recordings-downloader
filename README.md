# Zoom Recordings Downloader

A Python library to download Zoom users recordings

## Dependencias

* Python 3,6+
* Además de instalar los siguientes paquetes requeridos:
   * zoomus
   * python-decouple
   * python-dateutil

En sistemas Debian puede instalar las dependencias necesarias así:
```
`apt install python3-venv python3-pip`
`pip3 install zoomus`
`pip3 install python-decouple`
`pip3 install python-dateutil`
```

## Uso

Primero deberá crear una JWT App accediendo con las credenciales de su cuenta en el [Marketplace de Zoom](https://marketplace.zoom.us/) para lo cual se recomiendoa seguir [esta documentación](https://marketplace.zoom.us/docs/guides/build/jwt-app).

Luego de esto deberá crear un archivo `.env` dentro del mismo directorio donde ubique la librería `zoom_recordings.py`. Puede tomar como referencia el ejemplo [`example.env`](example.env). El `.env` es el archivo de configuración de la librería. Allí deberá indicar entre otras cosas:
* las credenciales (`API_KEY` y `API_SECRET`) de su JWT App recientemente creada.
* la fecha incial (`start_year`, `start_month`, `start_day_of_month`) a partir de la cual se quieren seleccionar las grabaciones (por su fecha de grabación).
* rutas de directorios para ubicar las grabaciones descargadas (`download_root_path`) y los logs (`log_dir_path`).

Por último, para usar la librería `zoom_recordings.py`, puede crear otro archivo .py donde importar la funcion `download_recordings` y personalizar su invocación. Esta función recibe por parámetro la lista de usuarios (`users_selected`) para los cuales se desean descargar sus grabaciones. A continuación un ejemplo de su utilización:

```
from zoom_recordings import download_recordings

users_selected=["user01@example.com","user02@example.com"]
download_recordings(users_selected)
```

Puede encontrar otro ejemplo en [`example_main.py`](example_main.py)
