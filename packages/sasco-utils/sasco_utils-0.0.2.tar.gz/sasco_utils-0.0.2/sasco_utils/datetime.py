# -*- coding: utf-8 -*-

"""
Python Utils by SASCO
Copyright (C) SASCO SpA (https://sasco.cl)

Este programa es software libre: usted puede redistribuirlo y/o modificarlo
bajo los términos de la GNU Lesser General Public License (LGPL) publicada
por la Fundación para el Software Libre, ya sea la versión 3 de la Licencia,
o (a su elección) cualquier versión posterior de la misma.

Este programa se distribuye con la esperanza de que sea útil, pero SIN
GARANTÍA ALGUNA; ni siquiera la garantía implícita MERCANTIL o de APTITUD
PARA UN PROPÓSITO DETERMINADO. Consulte los detalles de la GNU Lesser General
Public License (LGPL) para obtener una información más detallada.

Debería haber recibido una copia de la GNU Lesser General Public License
(LGPL) junto a este programa. En caso contrario, consulte
<http://www.gnu.org/licenses/lgpl.html>.
"""

from datetime import date, datetime, timedelta


def period_current():
    return int(date.today().strftime('%Y%m'))

def period_previous(period = None):
    if period is None:
        period = period_current()
    previous_period = period - 1
    if len(str(period)) == 6 and int(str(previous_period)[4:]) == 0:
        previous_period = previous_period - 100 + 12
    return previous_period

def period_next(period = None):
    if period is None:
        period = period_current()
    next_period = period + 1
    if len(str(period)) == 6 and int(str(next_period)[4:]) == 13:
        next_period = next_period + 100 - 12
    return next_period

def period_range(period_from, period_to = None):
    if period_to is None:
        period_to = period_current()
    periods = []
    period = period_from
    while period <= period_to :
        periods.append(period)
        period = period_next(period)
    return periods

def period_first_day(period):
    return str(period)[0:4]+'-'+str(period)[4:]+'-01'

def period_last_day(period):
    first_day_next_period = period_first_day(period_next(period))
    first_day_next_period_object = datetime.strptime(first_day_next_period, '%Y-%m-%d')
    last_day_object = first_day_next_period_object - timedelta(days=1)
    return last_day_object.strftime('%Y-%m-%d')

def date_add_days(days, from_date = None):
    if from_date is None:
        from_date = str(date.today().strftime('%Y-%m-%d'))
    y, m, d = from_date.split('-')
    specific_date = datetime(int(y), int(m), int(d))
    new_date = specific_date + timedelta(days = days)
    return str(new_date).split(' ')[0]

def date_count_days(date_from, date_to = None):
    if date_to is None:
        date_to = str(date.today().strftime('%Y-%m-%d'))
    y_from, m_from, d_from = str(date_from).split(' ')[0].split('-')
    y_to, m_to, d_to = str(date_to).split(' ')[0].split('-')
    delta = date(int(y_to), int(m_to), int(d_to)) - date(int(y_from), int(m_from), int(d_from))
    return delta.days if delta.days >= 0 else delta.days * -1
