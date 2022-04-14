import signal
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src import config, auth, other, channel_expansion, messages, channels, dm, channel, admin, user, notifications, search


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

def return_int_helper(num):
    if num != None:
        if (isinstance(num, int) == False) and (num.isdigit() == False):
            num = None
        else:
            num = int(num)
    return num

@APP.route("/auth/register/v2", methods=['POST'])
def handle_auth_register():
    request_data = request.get_json()
    email = request_data.get("email", None)
    if email != None:
        email = str(email)
    password = request_data.get("password", None)
    if password != None:
        password = str(password)
    name_first = request_data.get("name_first", None)
    if name_first != None:
        name_first = str(name_first)
    name_last = request_data.get("name_last", None)
    if name_last != None:
        name_last = str(name_last)

    return dumps(auth.auth_register_v1(email, password, name_first, name_last))


@APP.route("/auth/login/v2", methods=['POST'])
def handle_auth_login():
    request_data = request.get_json()
    email = request_data.get("email", None)
    if email != None:
        email = str(email)
    password = str(request_data.get("password", None))
    if password != None:
        password = str(password)

    return dumps(auth.auth_login_v1(email, password))

@APP.route("/channel/leave/v1", methods=['POST'])
def handle_channel_leave():
    request_data = request.get_json()
    token = str(request_data.get("token", None))
    if token != None:
        token = str(token)
    channel_id = request_data.get("channel_id", None)
    channel_id = return_int_helper(channel_id)

    return dumps(channel_expansion.channel_leave_v1(token, channel_id))

@APP.route("/channels/listall/v2", methods=['GET'])
def channel_listall():
    token = str(request.args.get('token'))

    return dumps(channels.channels_listall_v1(token))

@APP.route("/channel/details/v2", methods=['GET'])
def channel_details():
    token = str(request.args.get('token', None))
    channel_id = request.args.get('channel_id', None)
    channel_id = return_int_helper(channel_id)
    
    return dumps(channel.channel_details_v1(token, channel_id))

@APP.route("/channel/addowner/v1", methods=['POST'])
def handle_channel_addowner():
    request_data = request.get_json()
    token = request_data.get("token", None)
    if token != None:
        token = str(token)
    channel_id = request_data.get("channel_id", None)
    channel_id = return_int_helper(channel_id)
    u_id = request_data.get("u_id", None)
    u_id = return_int_helper(u_id)

    return dumps(channel_expansion.channel_addowner_v1(token, channel_id, u_id))

@APP.route("/channel/removeowner/v1", methods=["POST"])
def handle_channel_removeowner():
    request_data = request.get_json()
    token = request_data.get("token", None)
    if token != None:
        token = str(token)
    channel_id = request_data.get("channel_id", None)
    channel_id = return_int_helper(channel_id)
    u_id = request_data.get("u_id", None)
    u_id = return_int_helper(u_id)

    return dumps(channel_expansion.channel_removeowner_v1(token, channel_id, u_id))

@APP.route("/auth/logout/v1", methods=['POST'])
def handle_auth_logout():
    request_data = request.get_json()
    token = request_data.get("token", None)
    if token != None:
        token = str(token)

    return dumps(auth.auth_logout_v1(token))


@APP.route("/message/send/v1", methods=['POST'])
def handle_message_send():
    request_data = request.get_json()
    token = request_data.get("token", None)
    if token != None:
        token = str(token)
    channel_id = request_data.get("channel_id", None)
    channel_id = return_int_helper(channel_id)
    message = request_data.get("message", None)
    if message != None:
        message = str(message)

    return dumps(messages.message_send_v1(token, channel_id, message))


@APP.route("/message/senddm/v1", methods=['POST'])
def handle_message_senddm():
    request_data = request.get_json()
    token = request_data.get("token", None)
    if token != None:
        token = str(token)
    dm_id = request_data.get("dm_id", None)
    dm_id = return_int_helper(dm_id)
    message = request_data.get("message", None)
    if message != None:
        message = str(message)

    return dumps(messages.message_senddm_v1(token, dm_id, message))


@APP.route("/channels/create/v2", methods=['POST'])
def handle_channels_create():
    request_data = request.get_json()
    name = request_data.get("name", None)
    if name != None:
        name = str(name)
    is_public = request_data.get("is_public")
    if isinstance(is_public, bool) == False:
        is_public = None
    token = request_data.get("token", None)
    if token != None:
        token = str(token)
    return dumps(channels.channels_create_v1(token, name, is_public))


@APP.route("/dm/remove/v1", methods=['DELETE'])
def handle_dm_delete():
    request_data = request.get_json()
    token = str(request_data.get("token", None))
    dm_id = request_data.get("dm_id", None)
    dm_id = return_int_helper(dm_id)
    dm.dm_remove_v1(token, dm_id)
    
    return dumps({})


@APP.route("/channels/list/v2", methods=['GET'])
def handle_channels_list():
    token = str(request.args.get('token'))
    return dumps(channels.channels_list_v1(token))

@APP.route("/channel/messages/v2", methods=['GET'])
def handle_channel_messages():

    token = str(request.args.get('token'))

    channel_id = request.args.get('channel_id', None)
    channel_id = return_int_helper(channel_id)

    start = request.args.get('start', None)
    start = return_int_helper(start)

    return_value = channel.channel_messages_v1(token, channel_id, start)

    return dumps(return_value)

@APP.route("/dm/list/v1", methods=['GET'])
def handle_dms_list():
    token = str(request.args.get('token'))
    return dumps(dm.dm_list_v1(token))


@APP.route("/dm/details/v1", methods=['GET'])
def handle_dms_details():
    token = str(request.args.get('token'))
    dm_id = request.args.get('dm_id')
    dm_id = return_int_helper(dm_id)
    return dumps(dm.dm_details_v1(token, dm_id))

@APP.route("/dm/messages/v1", methods=['GET'])
def dm_messages():
    token = str(request.args.get('token', None))
    
    dm_id = request.args.get('dm_id', None)
    dm_id = return_int_helper(dm_id)
    
    start = request.args.get('start', None)
    start = return_int_helper(start)
    
    return dumps(dm.dm_messages_v1(token, dm_id, start))


@ APP.route("/clear/v1", methods=['DELETE'])
def handle_clear():
    other.clear_v1()
    return dumps({})


@ APP.route("/admin/userpermission/change/v1", methods=['POST'])
def handle_userpermission_change():
    request_data = request.get_json()
    token = request_data.get("token", None)
    if token != None:
        token = str(token)

    u_id = request_data.get("u_id", None)
    u_id = return_int_helper(u_id)
    permission_id = request_data.get("permission_id", None)
    permission_id = return_int_helper(permission_id)

    return dumps(admin.admin_userpermission_change(token, u_id, permission_id))


@ APP.route("/dm/create/v1", methods=['POST'])
def dm_create():
    request_data = request.get_json()
    token = str(request_data.get("token", None))
    u_ids = list(request_data.get("u_ids", []))

    return dumps(dm.dm_create_v1(token, u_ids))


@APP.route("/dm/leave/v1", methods=['POST'])
def dm_leave():
    request_data = request.get_json()
    token = request_data.get('token', None)
    if token != None:
        token = str(token)
    dm_id = request_data.get("dm_id", None)
    dm_id = return_int_helper(dm_id)
    
    return dumps(dm.dm_leave_v1(token, dm_id))


@APP.route("/channel/invite/v2", methods=['POST'])
def handle_channel_invite():
    request_data = request.get_json()
    token = str(request_data.get("token", None))
    channel_id = request_data.get("channel_id", None)
    channel_id = return_int_helper(channel_id)
    u_id = request_data.get("u_id", None)
    u_id = return_int_helper(u_id)

    return dumps(channel.channel_invite_v1(token, channel_id, u_id))


@ APP.route("/channel/join/v2", methods=['POST'])
def handle_channel_join():
    request_data = request.get_json()
    token = str(request_data.get("token", None))
    channel_id = request_data.get("channel_id", None)
    channel_id = return_int_helper(channel_id)

    return dumps(channel.channel_join_v1(token, channel_id))

@APP.route("/user/profile/v1", methods=['GET'])
def handle_user_profile():
    
    token = request.args.get("token", None)
    u_id = request.args.get("u_id", None)
    u_id = return_int_helper(u_id)

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

@APP.route("/message/edit/v1", methods=['PUT'])
def handle_message_edit():
    request_data = request.get_json()
    token = str(request_data.get("token", None))
    message_id = request_data.get("message_id", None)
    message_id = return_int_helper(message_id)
    message = str(request_data.get("message", None))

    return dumps(messages.message_edit_v1(token, message_id, message))

@APP.route("/message/remove/v1", methods=['DELETE'])
def hendle_message_remove():
    request_data = request.get_json()
    token = str(request_data.get("token", None))
    message_id = request_data.get("message_id", None)
    message_id = return_int_helper(message_id)

    return dumps(messages.message_remove_v1(token, message_id))

@APP.route("/admin/user/remove/v1", methods=['DELETE'])
def handle_admin_user_remove():
    request_data = request.get_json()
    token = str(request_data.get("token", None))
    u_id = int(request_data.get("u_id", None))

    return dumps(admin.admin_user_remove(token, u_id))


@APP.route("/users/all/v1", methods=['GET'])
def users_all():
    token = str(request.args.get('token', None))

    return dumps(user.users_all_v1(token))


@APP.route("/notifications/get/v1", methods=['GET'])
def handle_notifications_get():
    token = request.args.get("token", None)
    if token != None:
        token = str(token)

    return dumps(notifications.notifications_get(token))


@APP.route("/search/v1", methods=['GET'])
def handle_search():
    token = request.args.get("token", None)
    if token != None:
        token = str(token)
    query_str = request.args.get("query_str", None)
    if query_str != None:
        query_str = str(query_str)
    
    return dumps(search.search_v1(token, query_str))


@APP.route("/message/share/v1", methods=["POST"])
def handle_message_share():
    request_data = request.get_json()
    token = str(request_data.get("token", None))
    og_message_id = int(request_data.get("og_message_id", None))
    message = str(request_data.get("message", None))
    channel_id = int(request_data.get("channel_id", None))
    dm_id = int(request_data.get("dm_id", None))

    return dumps(messages.message_share_v1(token, og_message_id, message, channel_id, dm_id))

@APP.route("/message/sendlater/v1", methods=["POST"])
def handle_message_sendlater():
    request_data = request.get_json()
    token = str(request_data.get("token", None))
    channel_id = int(request_data.get("channel_id", None))
    message = str(request_data.get("message", None))
    time_sent = int(request_data.get("time_sent", None))

    return dumps(messages.message_sendlater_v1(token, channel_id, message, time_sent))

@APP.route("/message/sendlaterdm/v1", methods=["POST"])
def handle_message_sendlaterdm():
    request_data = request.get_json()
    token = str(request_data.get("token", None))
    dm_id = int(request_data.get("dm_id", None))
    message = str(request_data.get("message", None))
    time_sent = int(request_data.get("time_sent", None))

    return dumps(messages.message_sendlaterdm_v1(token, dm_id, message, time_sent))

# NO NEED TO MODIFY BELOW THIS POINT


if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port
