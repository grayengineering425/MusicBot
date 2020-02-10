from flask          import Flask, request, jsonify
from flask_cors     import CORS
from Server         import Server
from AppSettings    import AppSettings

import datetime

appSettings = AppSettings()

app     = Flask  (__name__ )
CORS(app)
server  = Server (appSettings)

#All events come in through POST requests
@app.route('/', methods=['POST'])
def Event():
    #Initial error checking, ensure type of message is JSON and we have base data needed to continue
    if not request.json:
        return jsonify({'error' : "Invalid payload type, only json permitted"}), 400
    if not 'token' in request.json:
        return jsonify({'error' : "missing required value, token"}), 400
    if not 'type' in request.json:
        return jsonify({'error' : "missing required value, type" }), 400
    
    token = request.json['token']
    
    if token != appSettings.slackVerificationToken:
        return jsonify({'forbidden' : "Tokens do not match"}), 403

    #Check the type of the message, then allow server to handle business logic based on the event
    type = request.json['type']

    if type == 'url_verification':
        challenge = request.json['challenge']
    
        return jsonify({'challenge': challenge}), 200

    if not 'event' in request.json:
        return jsonify({'error' : "missing required value, event"}), 400

    event = request.json['event']

    if not 'type' in event:
        return jsonify({'error' : "missing required value, event->type"}), 400
    
    eventType  = event['type']

    if eventType == 'app_mention':
        server.handleAppMention(event)

        return jsonify({'success': True}), 200

    elif eventType == 'link_shared':
        print('someone shared a spotify link!')

        server.handleLinkPosted(event)

        return jsonify({'success': True}), 200

    #If we get here, the request is not currently  supported
    return jsonify({'not supported': 'the request is not currently supported by the server'}), 405

@app.route('/spotify', methods=['POST'])
def slashSpotify():
    print('received request!')

    j = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "https://open.spotify.com/user/yeprx0m3tflw7451xg0wqpp1x?si=n1Fd4afWSnCfWPuvFAsmOw"
                }
            }
        ]
    }

    return jsonify(j), 200
