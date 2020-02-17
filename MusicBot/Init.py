import os
import sys
import datetime

sys.path.append(os.getcwd() + '/Settings'       )
sys.path.append(os.getcwd() + '/WebApis'        )
sys.path.append(os.getcwd() + '/Localization'   )
sys.path.append(os.getcwd() + '/Data'           )

from flask          import Flask, request, jsonify
from flask_cors     import CORS
from Server         import Server, SlashRequests
from AppSettings    import AppSettings

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
        server.handleLinkPosted(event)

        return jsonify({'success': True}), 200

    #If we get here, the request is not currently  supported
    return jsonify({'not supported': 'the request is not currently supported by the server'}), 405

@app.route('/spotify', methods=['POST'])
def slashSpotify():
    response = server.handleSlashRequest(SlashRequests.Spotify)
    
    return jsonify(response), 200


@app.route('/musicbotinfo', methods=['POST'])
def slashMusicBotInfo():
    response = server.handleSlashRequest(SlashRequests.MusicBotInfo)

    return jsonify(response), 200

@app.route('/github', methods=['POST'])
def slashGitHub():
    response = server.handleSlashRequest(SlashRequests.Github)

    return jsonify(response), 200
