#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name

# Copyright:
#   2020 P. H. <github.com/perfide>
# License:
#   AGPL-3.0-only (GNU Affero General Public License v3.0 only)
#   https://spdx.org/licenses/AGPL-3.0-only.html

"""Mask Database

Start a Gunicorn Test Server
"""

# included
import multiprocessing

# 3rd-party
import gunicorn.app.base

# internal
from maskdb import app

HOST = '0.0.0.0'
PORT = 5000


class UnicornApp(gunicorn.app.base.BaseApplication):  # pylint: disable=abstract-method;  # noqa: E501
    """App-definition for unicorn"""
    def __init__(self, _application, _options=None):
        self._options = _options or {}
        self._application = _application
        super().__init__()

    def load_config(self):
        for (key, value) in self._options.items():
            if key in self.cfg.settings and value is not None:
                self.cfg.set(key, value)

    def load(self):
        return self._application


if __name__ == '__main__':
    workers = 1 + 2 * multiprocessing.cpu_count()
    try:
        options = {
            'bind': '{}:{}'.format(HOST, PORT),
            'workers': workers,
        }
        unicorn_app = UnicornApp(app, options)
        unicorn_app.run()
    except KeyboardInterrupt:
        print('interrupted by keyboard')

# [EOF]
