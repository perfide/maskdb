#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright:
#   2020 P. H. <github.com/perfide>
# License:
#   AGPL-3.0-only (GNU Affero General Public License v3.0 only)
#   https://spdx.org/licenses/AGPL-3.0-only.html

"""Mask Database

Initialise sub-modules, translation and db-connection
"""

# included
import os
import string
import struct
import sys

# 3rd-party
from flask import Flask, request
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy


def get_app_config_dir() -> str:
    """Get the application share dir for templates and translations

    Args:
        None

    Returns:
        The applications config directory

    """
    if 'XDG_CONFIG_HOME' in os.environ:
        configs_dir = os.environ['XDG_CONFIG_HOME']
    elif 'APPDATA' in os.environ:
        configs_dir = os.environ['APPDATA']
    elif 'HOME' in os.environ:
        configs_dir = os.path.join(os.environ['HOME'], '.config')
    else:
        configs_dir = os.path.expanduser('~')

    app_config_dir = os.path.join(configs_dir, 'maskdb')
    return app_config_dir


def get_app_share_dir() -> str:
    """Get the application share dir for templates and translations

    Args:
        None

    Returns:
        The application static files directory

    """
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # for pyinstaller
        app_share_dir = sys._MEIPASS  # pylint: disable=no-member,protected-access;  # noqa: E501
    else:
        app_share_dir = os.path.abspath(os.path.dirname(__file__))
    return app_share_dir


def rand_index(size):
    """Secure replacement for random.random()*size

    Args:
        size (int): number of items

    Returns:
        int: A random value between 0 and size-1

    """
    rand_bytes = os.urandom(4)
    rand_no = struct.unpack('I', rand_bytes)[0]
    res = size * rand_no // 0x100000000
    return res


def generate_password(string_length=12):
    """Generate a random string of letters and digits

    Args:
        string_length (int): The target length of the password

    Returns:
        str: A secure password

    """
    letters_and_digits = string.ascii_letters + string.digits
    count = len(letters_and_digits)
    password = ''.join(
        letters_and_digits[rand_index(count)] for i in range(string_length)
    )
    return password


APP_CONFIG_DIR = get_app_config_dir()
print('APP_CONFIG_DIR {}'.format(APP_CONFIG_DIR))
APP_SHARE_DIR = get_app_share_dir()
print('APP_SHARE_DIR {}'.format(APP_SHARE_DIR))

TEMPLATE_FOLDER = os.path.join(APP_SHARE_DIR, 'templates')
TRANSLATION_DIRECTORY = os.path.join(APP_SHARE_DIR, 'translations')

if not os.path.exists(APP_CONFIG_DIR):
    os.makedirs(APP_CONFIG_DIR)
DATABASE_PATH = os.path.join(APP_CONFIG_DIR, 'customer.sqlite')
APP_CONFIG_PATH = os.path.join(APP_CONFIG_DIR, 'application.cfg')

if not os.path.exists(APP_CONFIG_PATH):
    SECRET_KEY = generate_password(string_length=16)
    with open(APP_CONFIG_PATH, 'w') as file_handler:
        file_handler.write('SECRET_KEY = "{}"'.format(SECRET_KEY))


class DefaultConfig:  # pylint: disable=too-few-public-methods
    """App config"""

    BABEL_TRANSLATION_DIRECTORIES = TRANSLATION_DIRECTORY
    DATE_FORMAT = '%d.%m.%Y'
    DATETIME_FORMAT = '%d.%m.%Y %H:%M'
    LANGUAGES = ('de', 'en')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(DATABASE_PATH)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app = Flask(__name__, template_folder=TEMPLATE_FOLDER)  # pylint: disable=invalid-name;  # noqa: E501
app.config.from_object(DefaultConfig)
app.config.from_pyfile(APP_CONFIG_PATH, silent=False)
db = SQLAlchemy(app)  # pylint: disable=invalid-name
babel = Babel(app)  # pylint: disable=invalid-name


@babel.localeselector
def get_locale() -> str:
    """Get the locale from flask for every request"""
    lang = request.accept_languages.best_match(app.config['LANGUAGES'])
    print('get_locale: {}'.format(lang))
    return lang


# just for init
from . import models  # pylint: disable=wrong-import-position;  # noqa: F401,E402,E501
from . import views  # pylint: disable=cyclic-import,wrong-import-position;  # noqa: F401,E402,E501

# [EOF]
