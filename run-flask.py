#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name

# Copyright:
#   2020 P. H. <github.com/perfide>
# License:
#   AGPL-3.0-only (GNU Affero General Public License v3.0 only)
#   https://spdx.org/licenses/AGPL-3.0-only.html

"""Mask Database

Start a Flask Debug Server
"""

# 3rd-party
from flask_babel import _

# internal
from maskdb import app

HOST = '0.0.0.0'
PORT = 5000

if __name__ == '__main__':
    try:
        app.run(debug=True, host=HOST, port=PORT)
    except OSError as err:
        if err.errno == 98:
            print(
                _(
                    'The address "%(host)s:%(port)s" is already in use',
                    host=HOST,
                    port=PORT,
                )
            )
        else:
            print(err)
    except KeyboardInterrupt:
        print('interrupted by keyboard')

# [EOF]
