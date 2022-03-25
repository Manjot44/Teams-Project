import sys
import signal
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config, auth, channel_expansion, other

def quit_gracefully(*args):
    '''For coverage'''
    exit(0)

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

#### NO NEED TO MODIFY ABOVE THIS POINT, EXCEPT IMPORTS

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
        raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

@APP.route("/auth/register/v2", methods=['POST'])
def handle_auth_register():
    request_data = request.get_json()
    email = str(request_data.get("email", None))
    password = str(request_data.get("password", None))
    name_first = str(request_data.get("name_first", None))
    name_last = str(request_data.get("name_last", None))

    return dumps(auth.auth_register_v1(email, password, name_first, name_last))

@APP.route("/auth/login/v2", methods=['POST'])
def handle_auth_login():
    request_data = request.get_json()
    email = str(request_data.get("email", None))
    password = str(request_data.get("password", None))

    return dumps(auth.auth_login_v1(email, password))

@APP.route("/auth/logout/v1", methods=['POST'])
def handle_auth_logout():
    request_data = request.get_json()
    token = str(request_data.get("token", None))

    return dumps(auth.auth_logout_v1(token))

@APP.route("/channel/leave/v1", methods=['POST'])
def handle_channel_leave():
    request_data = request.get_json()
    token = str(request_data.get("token", None))
    channel_id = int(request_data.get("channel_id", None))

    return dumps(channel_expansion.channel_leave_v1(token, channel_id))

@APP.route("/channel/addowner/v1", methods=['POST'])
def handle_channel_addowner():
    request_data = request.get_json()
    token = str(request_data.get("token", None))
    channel_id = int(request_data.get("channel_id", None))
    u_id = int(request_data.get("u_id", None))

    return dumps(channel_expansion.channel_addowner_v1(token, channel_id, u_id))

@APP.route("/channel/removeowner/v1", methods=["POST"])
def handle_channel_removeowner():
    request_data = request.get_json()
    token = str(request_data.get("token", None))
    channel_id = int(request_data.get("channel_id", None))
    u_id = int(request_data.get("u_id", None))

    return dumps(channel_expansion.channel_removeowner_v1(token, channel_id, u_id))

@APP.route("/clear/v1", methods=['DELETE'])
def handle_clear():
    other.clear_v1()
    return dumps({})


#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port
