
# MaskDB
A simple web-service to register customers by name and birthday

## Install

### Docker

Just call `docker-compose up` and visit [localhost](http://127.0.0.1:5000/)!

### Python (debug)

Install dependencies with `pip install -r requirements.txt`.

#### Flask-Debug

Execute `./flask-debug.py` to start with the integrated Flask web-server.
Visit [localhost](http://127.0.0.1:5000/)!

#### Gunicorn

Exeute `./gunicorn-debug.sh` to listen on all IPs.
Visit [localhost](http://127.0.0.1:5000/)!


## Update Translations

Fetch messages from the code and create messages.pot

    pybabel extract -F babel.cfg -k lazy_gettext -k _l -o messages.pot .

Update the po-files in the translation directory

    pybabel update -i messages.pot -d maskdb/translations/

Compile the mo-files

    pybabel compile -d maskdb/translations


## Thanks

The great tutorials from Miguel Grinberg gave some good hints on
how to structure and optimize this application.
See [The Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) and the corresponding github repo [microblog](https://github.com/miguelgrinberg/microblog)!
