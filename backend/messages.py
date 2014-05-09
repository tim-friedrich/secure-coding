import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote


class ItemMessage(messages.Message):
    title = messages.StringField(2)
    description = messages.StringField(3)
    expiration = messages.StringField(4)
    price = messages.StringField(5)
    owner = messages.MessageField("UserMessage", 6)
    item_id = messages.StringField(7)


class ItemMessageCollection(messages.Message):
    message = messages.StringField(1)
    code = messages.StringField(2)
    data = messages.MessageField(ItemMessage, 3, repeated=True)


class BaseMessage(messages.Message):
    message = messages.StringField(1)
    code = messages.StringField(2)
    data = messages.StringField(3)


class UserMessage(messages.Message):
    user_id = messages.StringField(1)
    email = messages.StringField(2)
    name = messages.StringField(3)
    description = messages.StringField(4)
    image_url = messages.StringField(5)
    tag = messages.StringField(6)
    disabled = messages.StringField(7)


class UserMessageCollection(messages.Message):
    message = messages.StringField(1)
    code = messages.StringField(2)
    data = messages.MessageField(UserMessage, 3, repeated=True)


class CommMessage(messages.Message):
    subject = messages.StringField(1)
    sender = messages.StringField(2)
    receiver = messages.StringField(3)
    timestamp = messages.StringField(4)
    content = messages.StringField(5)
    item_id = messages.StringField(6)
    item_title = messages.StringField(7)
    price = messages.StringField(8)


class CommMessageCollection(messages.Message):
    message = messages.StringField(1)
    code = messages.StringField(2)
    data = messages.MessageField(CommMessage, 3, repeated=True)