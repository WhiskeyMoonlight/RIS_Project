import os

from flask import (
    Blueprint, render_template,
    request, current_app,
    session, redirect, url_for
)

from access import group_required
from database.operations import select, call_procedure
from database.sql_provider import SQLProvider

blueprint_report = Blueprint(
    'blueprint_report',
    __name__,
)

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_report.route('/', methods=['GET'])
@group_required
def index():
    return render_template('reports/base.html')


@blueprint_report.route('/report', methods=['GET'])
@group_required
def work_report():
    return render_template('reports/chosen_report.html')


@blueprint_report.route('/create', methods=['GET', 'POST'])
@group_required
def create_report():
    if request.method == 'GET':
        return render_template('reports/date_form.html')
    else:
        db_config = current_app.config['db_config']

        year = request.form.get('year')
        month = request.form.get('month')

        sql = provider.get('select_report_date.sql', year=year, month=month)
        reports = select(db_config, sql)

        if reports:
            return render_template('reports/date_form.html',
                                   error='Такой отчёт уже существует')

        reports = call_procedure(db_config, 'create_otchet', year, month)

        if not reports:
            return render_template('reports/date_form.html',
                                   error=f'Отчёт не создан. За {month}-{year} заказов нет.')

        return render_template('reports/successful_report.html', year=year, month=month)


@blueprint_report.route('/view/<date>', methods=['GET'])
@group_required
def view_report(date):
    db_config = current_app.config['db_config']

    year = int(date[:4])
    month = int(date[5:])

    sql = provider.get('select_report_date.sql', year=year, month=month)
    reports = select(db_config, sql)

    return render_template('reports/report_view.html', reports=reports, date=date)
