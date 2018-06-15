import graphene

from graphene_django.types import DjangoObjectType

from bootcamp.messager.models import Message


class MessageType(DjangoObjectType):
    """DjangoObjectType to acces the Message model."""

    class Meta:
        model = Message


class MessageQuery(object):
    """Abstract object to register in the root schema, allowing to query the
    model."""
    conversation = graphene.List(MessageType)

    def resolve_conversation(self, info, **kwargs):
        """Resolves a required conversation between two registered users."""
        sender = kwargs["sender"]
        recipient = kwargs["recipient"]
        return Message.objects.get_conversation(sender, recipient)

    def resolve_message(self, info, **kwargs):
        uuid_id = kwargs.get('uuid_id')

        if uuid_id is not None:
            return Message.objects.get(uuid_id=uuid_id)

        return None
