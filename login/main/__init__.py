from flask import Blueprint, render_template, session
from flask_login import login_required

main = Blueprint('main', __name__)


@main.route('/public')
def public_page():
    session['page'] = 'public'
    return render_template('main/public.html')


@main.route('private')
# login을 한 상태에서만 접근이 가능하도록 해줌
@login_required
def private_page():
    session['page'] = 'private'
    return render_template('main/private.html')


@main.route('session')
def session_page():
    return render_template('main/session.html')

