from flask import (Blueprint, jsonify, redirect, render_template, request,
                   url_for)
from sqlalchemy import or_

from app.extensions import db
from app.models.message import Message
from app.models.user import User

bp = Blueprint('chat', __name__,
               template_folder='../templates/communication',
               static_folder='static',
               static_url_path='communication')


@bp.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)


@bp.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    existing_user = User.query.filter_by(email=username).first()

    if existing_user:
        return redirect(url_for('chat', username=username))

    new_user = User(email=username)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('chat', username=username))


@bp.route('/chat/<username>')
def chat(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return redirect(url_for('chat.index'))

    # Znajdź wszystkich użytkowników, z którymi dany użytkownik prowadził rozmowy
    chat_users = db.session.query(User).join(
        Message,
        or_(Message.sender_id == User.id, Message.receiver_id == User.id)
    ).filter(
        or_(Message.sender_id == user.id, Message.receiver_id == user.id)
    ).distinct().all()

    chat_users = [u for u in chat_users if u.username != username]

    return render_template('chat.html', user=user, chat_users=chat_users)


@bp.route('/search_users')
def search_users():
    current_username = request.args.get('current_username')
    query = request.args.get('query', '')

    users = User.query.filter(
        User.username.ilike(f'%{query}%'),
        User.username != current_username
    ).all()

    return jsonify([{'username': user.username} for user in users])


@bp.route('/get_messages')
def get_messages():
    sender_username = request.args.get('sender')
    receiver_username = request.args.get('receiver')

    sender = User.query.filter_by(username=sender_username).first()
    receiver = User.query.filter_by(username=receiver_username).first()

    if not sender or not receiver:
        return jsonify([])

    messages = Message.query.filter(
        or_(
            (Message.sender_id == sender.id) & (Message.receiver_id == receiver.id),
            (Message.sender_id == receiver.id) & (Message.receiver_id == sender.id)
        )
    ).order_by(Message.timestamp).all()

    return jsonify([{
        'sender': message.sender.username,
        'content': message.content,
        'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    } for message in messages])
