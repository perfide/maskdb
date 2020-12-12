#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright:
#   2020 P. H. <github.com/perfide>
# License:
#   AGPL-3.0-only (GNU Affero General Public License v3.0 only)
#   https://spdx.org/licenses/AGPL-3.0-only.html

"""Mask Database

Flask routes and its helper functions
"""

# included
import datetime

# 3rd-party
from flask import flash
from flask import render_template
from flask_babel import _
import sqlalchemy

# internal
from maskdb import app
from maskdb import db  # pylint: disable=cyclic-import
from maskdb.forms import SearchForm
from maskdb.models import Customer


def human_to_db_date(human_date: str) -> str:
    """Convert human date to DB-date"""
    return convert_utc_to_local(
        human_date,
        app.config['DATE_FORMAT'],
        '%Y%m%d',
    )


def db_to_human_date(db_date: str) -> str:
    """Convert date from DB to human-readable format"""
    return convert_utc_to_local(db_date, '%Y%m%d', app.config['DATE_FORMAT'])


def db_to_human_datetime(db_date: str) -> str:
    """Convert time from DB to human-readable format"""
    return convert_utc_to_local(
        db_date, '%Y%m%dT%H%MZ', app.config['DATETIME_FORMAT']
    )


def convert_utc_to_local(
    from_datetime: str, from_format: str, to_format: str
) -> str:
    """Interprete timestamp as from UTC and convert it to local time"""
    dt_instance = datetime.datetime.strptime(from_datetime, from_format)
    local_time = dt_instance.replace(tzinfo=datetime.timezone.utc).astimezone()
    to_datetime = local_time.strftime(to_format)
    return to_datetime


def db_to_human_customer(
    customer: 'maskdb.models.Customer',  # noqa: F821
) -> 'maskdb.models.Customer':  # noqa: F821
    """Convert DB data to human-readable output"""
    customer.birthday = db_to_human_date(customer.birthday)
    if customer.added_by is None:
        customer.added_by = '-'
    if customer.added_at is None:
        customer.added_at = '-'
    else:
        customer.added_at = db_to_human_datetime(customer.added_at)
    return customer


def search(form: 'maskdb.forms.SearchForm') -> list:  # noqa: F821
    """Handler for the search-button"""
    query = {}
    if form.first_name.data:
        query['first_name'] = form.first_name.data
    if form.surname.data:
        query['surname'] = form.surname.data
    if form.birthday.data:
        query['birthday'] = human_to_db_date(form.birthday.data)
    match = Customer.query.filter_by(**query)
    customers = []
    try:
        for customer in match.all():
            customers.append(db_to_human_customer(customer))
    except sqlalchemy.exc.OperationalError as err:
        flash(_('Database search failed: %(error)s', error=err.orig))
    return customers


def add(form: 'maskdb.forms.SearchForm') -> None:  # noqa: F821
    """Handler for the add-button"""
    if not form.first_name.data:
        flash(_('Add first name'))
        return
    if not form.surname.data:
        flash(_('Add surname'))
        return
    if not form.birthday.data:
        flash(_('Add birthday'))
        return
    if not form.added_by.data:
        flash(_('Add your name'))
        return
    customer = Customer(
        first_name=form.first_name.data,
        surname=form.surname.data,
        birthday=human_to_db_date(form.birthday.data),
        added_by=form.added_by.data,
        added_at=datetime.datetime.utcnow().strftime('%Y%m%dT%H%MZ'),
    )
    db.session.add(customer)  # pylint: disable=no-member
    try:
        db.session.commit()  # pylint: disable=no-member
    except sqlalchemy.exc.IntegrityError as err:
        if err.orig.args[0].startswith('UNIQUE constraint failed: '):
            flash(
                _(
                    'Customer %(first_name)s %(surname)s already exists',
                    first_name=form.first_name.data,
                    surname=form.surname.data,
                )
            )
        else:
            flash(_('Database rejected request: %(error)s', error=err.orig))
    except sqlalchemy.exc.OperationalError as err:
        flash(_('Database add failed: %(error)s', error=err.orig))
    else:
        flash(
            _(
                'Added %(first_name)s %(surname)s',
                first_name=form.first_name.data,
                surname=form.surname.data,
            )
        )
    return


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def route_index() -> str:
    """HTTP / and /index route"""
    print('route_index: {}'.format(_('default-lang')))
    count = 0
    customers = []
    form = SearchForm()
    if not form.validate_on_submit():
        # GET or invalid POST
        return render_template(
            'index.html', title=_('Search'), form=form, locale='de'
        )

    if form.search.data:
        customers = search(form)
        count = len(customers)
    else:
        add(form)

    html = render_template(
        'index.html',
        title=_('Search'),
        form=form,
        count=count,
        customers=customers,
        is_search=form.search.data,
    )
    return html


@app.route('/list')
def route_list():
    """HTTP /list route"""
    print('route_list: {}'.format(_('default-lang')))
    customers = []
    try:
        for customer in Customer.query.all():
            customers.append(db_to_human_customer(customer))
    except sqlalchemy.exc.OperationalError as err:
        flash(_('Database listing failed: %(error)s', error=err.orig))
    html = render_template(
        'list.html',
        title=_('List'),
        count=len(customers),
        customers=customers,
    )
    return html


# [EOF]
