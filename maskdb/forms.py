#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright:
#   2020 P. H. <github.com/perfide>
# License:
#   AGPL-3.0-only (GNU Affero General Public License v3.0 only)
#   https://spdx.org/licenses/AGPL-3.0-only.html

"""Mask Database

HTML-Forms using Flask-WTF
"""

# included
import datetime

# 3rd-party
from flask_babel import _, lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
)
from wtforms.validators import ValidationError

# internal
from maskdb import app


def validate_name(
    unused: 'SearchForm',  # pylint: disable=W0613
    field: StringField,
) -> None:
    """Validate first name and surname form fields"""
    if not field.data:
        return
    if len(field.data) < 2:
        raise ValidationError(_('Names too short'))
    if field.data[0].islower():
        raise ValidationError(_('Names should start uppercase'))
    if field.data[1].isupper():
        raise ValidationError(_('The second letter should be lowercase'))
    return


def validate_date(
    unused: 'SearchForm',  # pylint: disable=W0613
    field: StringField,
) -> None:
    """Validate date form fields"""
    if not field.data:
        return
    try:
        datetime.datetime.strptime(field.data, app.config['DATE_FORMAT'])
    except ValueError:
        date_format = app.config['DATE_FORMAT']
        date_format = date_format.replace('%Y', 'YYYY')
        date_format = date_format.replace('%m', 'MM')
        date_format = date_format.replace('%d', 'DD')
        message = _(
            'Please use the "%(date_format)s" format!',
            date_format=date_format,
        )
        raise ValidationError(message)
    return


class SearchForm(FlaskForm):  # pylint: disable=too-few-public-methods
    """Flask-WTF form definition"""

    first_name = StringField(_l('First name'), validators=[validate_name])
    surname = StringField(_l('Surname'), validators=[validate_name])
    birthday = StringField(_l('Birthday'), validators=[validate_date])
    added_by = StringField(_l('Added by'), validators=[validate_name])
    search = SubmitField(_l('Search'))
    add = SubmitField(_l('Add'))


# [EOF]
