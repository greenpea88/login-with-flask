from flask import Blueprint, render_template

main = Blueprint('main', __name__)


@main.route('/public')
def public_page():
    return render_template('main/public.html')


@main.route('private')
def private_page():
    return render_template('main/private.html')
