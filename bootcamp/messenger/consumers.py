import json

from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http


@channel_session_user_from_http
def ws_connect(message):
    message.reply_channel.send({"accept": True})
    Group('{}'.format(message.user)).add(message.reply_channel)


@channel_session_user
def ws_disconnect(message):
    Group('{}'.format(message.user)).discard(message.reply_channel)


def ws_receive(message):
    old_message = json.loads(message.content['text'])
    if old_message['activity_type'] == "set_status":
        Group('notifications').send({
            'text': json.dumps({
                'sender': old_message['sender'],
                'status': old_message['status'],
                'activity_type': old_message['activity_type']
            })
        })
