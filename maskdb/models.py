#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright:
#   2020 P. H. <github.com/perfide>
# License:
#   AGPL-3.0-only (GNU Affero General Public License v3.0 only)
#   https://spdx.org/licenses/AGPL-3.0-only.html

"""Mask Database

Database-Scheme using Flask-SQLAlchemy
"""

# 3rd-party
import sqlalchemy

# internal
from maskdb import db  # pylint: disable=cyclic-import


class Customer(db.Model):  # pylint: disable=too-few-public-methods
    """Database-Scheme for customers"""

    id = db.Column(  # pylint: disable=no-member
        db.Integer, primary_key=True,  # pylint: disable=no-member
    )
    first_name = db.Column(  # pylint: disable=no-member
        db.String(64), index=True, unique=False,  # pylint: disable=no-member
    )
    surname = db.Column(  # pylint: disable=no-member
        db.String(64), index=True, unique=False  # pylint: disable=no-member
    )
    birthday = db.Column(  # pylint: disable=no-member
        db.String(8), index=True, unique=False,  # pylint: disable=no-member
    )
    added_at = db.Column(  # pylint: disable=no-member
        db.String(14), index=True, unique=False,  # pylint: disable=no-member
    )
    added_by = db.Column(  # pylint: disable=no-member
        db.String(64), index=True, unique=False  # pylint: disable=no-member
    )


# unique index over full name and birthday
db.Index(  # pylint: disable=no-member
    'uniquePerson',
    Customer.first_name,
    Customer.surname,
    Customer.birthday,
    unique=True,
)

try:
    db.create_all()
except sqlalchemy.exc.OperationalError as err:
    print('Failed to create tables: {}'.format(err.orig))
    import sys
    sys.exit(1)
db.session.commit()  # pylint: disable=no-member

# [EOF]
