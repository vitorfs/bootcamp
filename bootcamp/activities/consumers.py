from channels import Group


def ws_connect(message):
    Group('notifications').add(message.reply_channel)


def ws_disconnect(message):
    Group('notifications').discard(message.reply_channel)   