# Zoom Recordings Downloader

> This [README in Spanish](README.es.md)

A Python library to download Zoom users recordings

## Arquitecture and requirements

To automatically access recordings for download, you must have a Zoom account with developer privilegies in Zoom platform. You can then dowonload the recordings of all the virtual rooms that your account has aqcces to.

The library is called from a program running in server or a local system with Python, and accesses Zoom platform ressources through an [API JWT](https://marketplace.zoom.us/docs/guides/auth/jwt).

## Dependencies on your system

* Python version 3.6 or higher
* Morover, you must install the following packages:
   * zoomus
   * python-decouple
   * python-dateutil

On Debian and debian-like systems, you can install the needed dependencies as follows: 
```
apt install python3-venv python3-pip
pip3 install zoomus`
pip3 install python-decouple
pip3 install python-dateutil
```

## Usage

First you must create a JWT App, accessing with your credentials inti the [Zoom Marketplace](https://marketplace.zoom.us/), following this [this documentation](https://marketplace.zoom.us/docs/guides/build/jwt-app).

Then, a `.env` file must be created, in the same directory as the library `zoom_recordings.py`. Teh [`example.env`](example.env) file gives a reference for this tasc. This `.env` file is the configuration file of the library. It must particularly contain:
* the credentials (`API_KEY` and `API_SECRET`) of the JWT App just created in the Zoom platform.
* the initial date (`start_year`, `start_month`, `start_day_of_month`) since when the script shall download recordings (according to their creation date).
* paths to save the downloaded recordings (`download_root_path`) and the logs (`log_dir_path`).

Finally, to run the library `zoom_recordings.py`, you can call it from a python program, creating another .py file to import the `download_recordings` and customize parameters. This function needs as parameters the list of users, or more precisely rooms (`users_selected`) which recordings you want to download. Heere is a use example:

```
from zoom_recordings import download_recordings

users_selected=["user01@example.com","user02@example.com"]
download_recordings(users_selected)
```

You can find another example in [`example_main.py`](example_main.py).
