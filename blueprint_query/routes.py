import os
from flask import Blueprint, render_template, request, current_app
from work_with_db import select_dict
from sql_provider import SQLProvider

blueprint_query = Blueprint('bp_query', __name__)
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_query.route('/')
def query_menu():
    return render_template('query_menu.html')


@blueprint_query.route('/banquet_report', methods=['GET', 'POST'])
def banquet_report():
    if request.method == 'GET':
        return render_template('requests/input_param.html')
    else:
        _month = request.form.get('month')
        _year = request.form.get('year')
        _sql = provider.get('banquet_report.sql', month=_month, year=_year)
        order = select_dict(current_app.config['db_config'], _sql)
        print(order)
        if order:
            prod_title = "Results:"
            return render_template('requests/banquet_report.html', orders=order, prod_title=prod_title)
        else:
            return render_template('requests/no_results.html')


@blueprint_query.route('/manager_report', methods=['GET', 'POST'])
def manager_report():
    if request.method == 'GET':
        return render_template('requests/input_param.html')
    else:
        _sql = provider.get('manager_report.sql')
        manager_data = select_dict(current_app.config['db_config'], _sql)
        if manager_data:
            prod_title = "Results:"
            return render_template('requests/manager_report.html',
                                   manager=manager_data, prod_title=prod_title)
        else:
            return render_template('requests/no_results.html')


@blueprint_query.route('/youngest_manager', methods=['GET'])
def youngest_manager():
    _sql = provider.get('youngest_manager.sql')
    manager_data = select_dict(current_app.config['db_config'], _sql)
    if manager_data:
        prod_title = 'Youngest manager data:'
        return render_template('requests/manager_data.html', manager=manager_data, prod_title=prod_title)
    else:
        return render_template('requests/no_results.html')


@blueprint_query.route('/manager_without_orders', methods=['GET', 'POST'])
def manager_without_orders():
    if request.method == 'GET':
        return render_template('requests/input_param.html')
    else:
        _month = request.form.get('month')
        _year = request.form.get('year')
        _sql = provider.get('manager_without_orders.sql', month=_month, year=_year)
        manager_data = select_dict(current_app.config['db_config'], _sql)
        if manager_data:
            prod_title = 'The lazy managers are:'
            return render_template('requests/manager_data.html', manager=manager_data, prod_title=prod_title)
        else:
            return render_template('requests/no_results.html')
