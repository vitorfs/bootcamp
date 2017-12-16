import json
from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http


@channel_session_user_from_http
def ws_connect(message):
    message.reply_channel.send({"accept": True})
    Group('inbox-{}'.format(
        message.user.username)).add(message.reply_channel)
    # Group('users').send({
    #     'text': json.dumps({
    #         'username': message.user.username,
    #         'is_logged_in': True
    #     })
    # })


@channel_session_user
def ws_disconnect(message):
    # Group('users').send({
    #     'text': json.dumps({
    #         'username': message.user.username,
    #         'is_logged_in': False
    #     })
    # })
    # Group('users').discard(message.reply_channel)
    Group('inbox-{}'.format(
        message.user.username)).discard(message.reply_channel)


def ws_receive(message):
    Group('inbox-{}'.format(message.user.username)).send({
        "text": json.dumps({
            "id": message.id,
            "content": message.content
        })
    })
