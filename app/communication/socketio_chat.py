from flask import Flask, Blueprint
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from models import User, Message
from app.extensions import db
from routes import init_routes, bp

socketio = SocketIO(bp)

init_routes(bp)

@socketio.on('send_message')
def handle_message(data):
    sender_username = data['sender']
    receiver_username = data['receiver']
    message_content = data['message']
    
    sender = User.query.filter_by(username=sender_username).first()
    receiver = User.query.filter_by(username=receiver_username).first()
    
    if sender and receiver:
        new_message = Message(
            sender_id=sender.id, 
            receiver_id=receiver.id, 
            content=message_content
        )
        db.session.add(new_message)
        db.session.commit()
        
        socketio.emit('receive_message', {
            'sender': sender_username, 
            'receiver': receiver_username, 
            'message': message_content
        }, room=receiver_username)

@socketio.on('join')
def on_join(data):
    username = data['username']
    socketio.emit('user_joined', {'username': username})

if __name__ == '__main__':
    socketio.run(bp, debug=True)