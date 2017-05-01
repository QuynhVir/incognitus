#!/usr/bin/python3
from flask import Flask, request
import CommandHandler
import config

app = Flask(__name__)

VERIFY_TOKEN = config.VERIFY

@app.route('/', methods=['GET'])
def handle_verification():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200

@app.route('/', methods=['POST'])
def handle_incoming_messages():
    data = request.json
    try:
        sender = data['entry'][0]['messaging'][0]['sender']['id']
        message = data['entry'][0]['messaging'][0]['message']['text'].decode('UTF-8')
    except:
    	pass
    try:
        postback = data['entry'][0]['messaging'][0]['postback']['payload']
    except:
        pass
    if 'message' in locals():
        CommandHandler.message(sender, message)
    if 'postback' in locals():
        CommandHandler.postback(sender, postback)
    return "ok"
 
if __name__ == '__main__':
    app.run(debug=True)