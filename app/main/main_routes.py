from flask import render_template

from app.main import main_blueprint


@main_blueprint.route('/index', methods=['GET', 'POST'])
def get_index():
    return render_template('index.html')
