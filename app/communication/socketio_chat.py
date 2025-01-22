from flask import Blueprint
from flask_socketio import SocketIO
from app.models.user import User
from app.models.message import Message
from app.extensions import db
from .routes import init_routes, bp  

socketio = SocketIO() 

init_routes(bp)

@socketio.on('send_message')
def handle_message(data):
    try:
        sender_email = data['sender']
        receiver_email = data['receiver']
        message_content = data['message']
        
        sender = User.query.filter_by(email=sender_email).first()
        receiver = User.query.filter_by(email=receiver_email).first()
        
        if sender and receiver:
            new_message = Message(
                sender_id=sender.id, 
                receiver_id=receiver.id, 
                content=message_content
            )
            db.session.add(new_message)
            db.session.commit()
            
            socketio.emit('receive_message', {
                'sender': sender_email, 
                'receiver': receiver_email, 
                'message': message_content
            }, room=receiver_email)
        else:
            print(f"Sender or receiver not found: {sender_email}, {receiver_email}")
    except Exception as e:
        db.session.rollback()
        print(f"Error handling message: {e}")

@socketio.on('join')
def on_join(data):
    email = data['email']
    socketio.emit('user_joined', {'username': email})
