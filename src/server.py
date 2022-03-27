import sys
import signal
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src.error_help import check_valid_token
from src import config, auth, other, channel_expansion, messages, channels, error_help, data_store, dm, channel, admin, user
import src.admin


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

# NO NEED TO MODIFY ABOVE THIS POINT, EXCEPT IMPORTS

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
    email = request_data.get("email", None)
    if email != None:
        str(email)
    password = request_data.get("password", None)
    if password != None:
        str(password)
    name_first = request_data.get("name_first", None)
    if name_first != None:
        str(name_first)
    name_last = request_data.get("name_last", None)
    if name_last != None:
        str(name_last)

    return dumps(auth.auth_register_v1(email, password, name_first, name_last))


@APP.route("/auth/login/v2", methods=['POST'])
def handle_auth_login():
    request_data = request.get_json()
    email = request_data.get("email", None)
    if email != None:
        str(email)
    password = str(request_data.get("password", None))
    if password != None:
        str(password)

    return dumps(auth.auth_login_v1(email, password))

@APP.route("/channel/leave/v1", methods=['POST'])
def handle_channel_leave():
    request_data = request.get_json()
    token = str(request_data.get("token", None))
    if token != None:
        str(token)
    channel_id = request_data.get("channel_id", None)
    if isinstance(channel_id, int) == False:
        channel_id = None

    return dumps(channel_expansion.channel_leave_v1(token, channel_id))

@APP.route("/channels/listall/v2", methods=['GET'])
def channel_listall():
    token = str(request.args.get('token')) 
    data = data_store.data_store.get()

    u_id = check_valid_token(token, data)

    return dumps(channels.channels_listall_v1(u_id))

@APP.route("/channel/details/v2", methods=['GET'])
def channel_details():
    token = str(request.args.get('token', None))
    channel_id = request.args.get('channel_id', None)
    if channel_id == None:
        channel_id = None
    else:
        channel_id = int(request.args.get('channel_id', None))

    data = data_store.data_store.get()
    u_id = check_valid_token(token, data)
    
    return dumps(channel.channel_details_v1(u_id, channel_id))

@APP.route("/channel/addowner/v1", methods=['POST'])
def handle_channel_addowner():
    request_data = request.get_json()
    token = request_data.get("token", None)
    if token != None:
        str(token)
    channel_id = request_data.get("channel_id", None)
    if isinstance(channel_id, int) == False:
        channel_id = None
    u_id = request_data.get("u_id", None)
    if isinstance(u_id, int) == False:
        u_id= None

    return dumps(channel_expansion.channel_addowner_v1(token, channel_id, u_id))

@APP.route("/auth/logout/v1", methods=['POST'])
def handle_auth_logout():
    request_data = request.get_json()
    token = request_data.get("token", None)
    if token != None:
        str(token)

    return dumps(auth.auth_logout_v1(token))


@APP.route("/message/send/v1", methods=['POST'])
def handle_message_send():
    request_data = request.get_json()
    token = request_data.get("token", None)
    if token != None:
        str(token)
    channel_id = request_data.get("channel_id", None)
    if isinstance(channel_id, int) == False:
        channel_id = None
    message = request_data.get("message", None)
    if message != None:
        str(message)

    return dumps(messages.message_send_v1(token, channel_id, message))


@APP.route("/channels/create/v2", methods=['POST'])
def handle_channels_create():
    request_data = request.get_json()
    store = data_store.data_store.get()
    auth_user_id = error_help.check_valid_token(
        request_data.get("token", None), store)
    name = request_data.get("name", None)
    if name != None:
        str(name)
    is_public = request_data.get("is_public")
    if isinstance(is_public, bool) == False:
        is_public = False

    return dumps(channels.channels_create_v1(auth_user_id, name, is_public))


@APP.route("/dm/remove/v1", methods=['DELETE'])
def handle_dm_delete():
    request_data = request.get_json()
    store = data_store.data_store.get()
    auth_user_id = error_help.check_valid_token(
        request_data.get("token", None), store)
    dm_id = int(request_data.get("dm_id", None))
    dm.dm_remove_v1(auth_user_id, dm_id)
    return dumps({})


@APP.route("/channels/list/v2", methods=['GET'])
def handle_channels_list():
    token = str(request.args.get('token'))
    store = data_store.data_store.get()
    auth_user_id = store["users"][error_help.check_valid_token(
        token, store)]["u_id"]

    return dumps(channels.channels_list_v1(auth_user_id))


@APP.route("/dm/list/v1", methods=['GET'])
def handle_dms_list():
    token = str(request.args.get('token'))
    store = data_store.data_store.get()
    u_id = store["users"][error_help.check_valid_token(
        token, store)]["u_id"]

    return dumps(dm.dm_list_v1(u_id))


@APP.route("/dm/details/v1", methods=['GET'])
def handle_dms_details():
    token = str(request.args.get('token'))
    dm_id = int(request.args.get('dm_id'))
    store = data_store.data_store.get()
    u_id = store["users"][error_help.check_valid_token(
        token, store)]["u_id"]

    return dumps(dm.dm_details_v1(u_id, dm_id))


@ APP.route("/clear/v1", methods=['DELETE'])
def handle_clear():
    other.clear_v1()
    return dumps({})


@ APP.route("/admin/userpermission/change/v1", methods=['POST'])
def handle_userpermission_change():
    request_data = request.get_json()
    token = request_data.get("token", None)
    if token != None:
        str(token)
    u_id = request_data.get("u_id", None)
    if isinstance(u_id, int) == False:
        u_id = None
    permission_id = request_data.get("permission_id", None)
    if isinstance(permission_id, int) == False:
        permission_id = None

    return dumps(src.admin.admin_userpermission_change(token, u_id, permission_id))


@ APP.route("/dm/create/v1", methods=['POST'])
def dm_create():
    request_data = request.get_json()
    token = str(request_data.get("token", None))
    u_ids = list(request_data.get("u_ids", []))

    return dumps(dm.dm_create_v1(token, u_ids))


@ APP.route("/channel/invite/v2", methods=['POST'])
def handle_channel_invite():
    request_data = request.get_json()
    token = str(request_data.get("token", None))
    channel_id = int(request_data.get("channel_id", None))
    u_id = int(request_data.get("u_id", None))
    store = data_store.data_store.get()

    auth_user_id = error_help.check_valid_token(token, store)

    return dumps(channel.channel_invite_v1(auth_user_id, channel_id, u_id))


@ APP.route("/channel/join/v2", methods=['POST'])
def handle_channel_join():
    request_data = request.get_json()
    token = str(request_data.get("token", None))
    channel_id = int(request_data.get("channel_id", None))
    store = data_store.data_store.get()

    auth_user_id = error_help.check_valid_token(token, store)

    return dumps(channel.channel_join_v1(auth_user_id, channel_id))

@APP.route("/user/profile/v1", methods=['GET'])
def handle_user_profile():
    
    token = request.args.get("token", None)
    u_id = int(request.args.get("u_id", None))

    return dumps(user.user_profile_v1(token, u_id))

@APP.route("/user/profile/setname/v1", methods=['PUT'])
def handle_user_profile_setname():
    request_data = request.get_json()

    token = request_data.get("token", None)
    name_first = str(request_data.get("name_first", None))
    name_last = str(request_data.get("name_last", None))

    return dumps(user.user_profile_setname_v1(token, name_first, name_last))

@APP.route("/user/profile/setemail/v1", methods=['PUT'])
def handle_user_profile_setemail():
    request_data = request.get_json()
    
    token = str(request_data.get("token", None))
    email = str(request_data.get("email", None))

    return dumps(user.user_profile_setemail_v1(token, email))

@APP.route("/user/profile/sethandle/v1", methods=['PUT'])
def handle_user_profile_sethandle():
    request_data = request.get_json()
    
    token = str(request_data.get("token", None))
    handle_str = str(request_data.get("handle_str", None))

    return dumps(user.user_profile_sethandle_v1(token, handle_str))

# NO NEED TO MODIFY BELOW THIS POINT


if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port
