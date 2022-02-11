from flask import Blueprint, render_template, session

main = Blueprint('main', __name__)


@main.route('/public')
def public_page():
    session['page'] = 'public'
    return render_template('main/public.html')


@main.route('private')
def private_page():
    session['page'] = 'private'
    return render_template('main/private.html')


@main.route('session')
def session_page():
    return render_template('main/session.html')

