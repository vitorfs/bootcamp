import json
from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http


@channel_session_user_from_http
def ws_connect(message):
    message.reply_channel.send({"accept": True})
    Group('inbox-{}'.format(
        message.user.username)).add(message.reply_channel)


@channel_session_user
def ws_disconnect(message):
    Group('inbox-{}'.format(
        message.user.username)).discard(message.reply_channel)


@channel_session_user
def ws_receive(message):
    print(dir(message))
    print("this line")
    Group('inbox-{}'.format(message.receiver)).send({
        "text": json.dumps({
            "content": message.content
        })
    })
