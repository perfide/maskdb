#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name

# Copyright:
#   2020 P. H. <github.com/perfide>
# License:
#   AGPL-3.0-only (GNU Affero General Public License v3.0 only)
#   https://spdx.org/licenses/AGPL-3.0-only.html

"""Mask Database

Start a Waitress Test Server
"""

# 3rd-party
import waitress

# internal
from maskdb import app

HOST = '0.0.0.0'
PORT = 5000

if __name__ == '__main__':
    waitress.serve(app, listen='{}:{}'.format(HOST, PORT))

# [EOF]
