from flask import Blueprint, request

import database as db

recieve_api = Blueprint('recieve_api', __name__)

@recieve_api.route('/incoming', methods=['POST'])
def incoming():
    
    messageKey = request.form["stripped-text"]
    try:
        db.incomingMessage.create(messageKey=messageKey)
    except:
        print("Failed to write incomingMessage to DB!")
    
    return "All is well!"