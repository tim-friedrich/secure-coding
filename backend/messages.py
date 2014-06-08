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
    created_at = messages.StringField(7)
    item_id = messages.StringField(8)


class ItemMessageCollection(messages.Message):
    message = messages.StringField(1)
    code = messages.StringField(2)
    data = messages.MessageField(ItemMessage, 3, repeated=True)


class BaseMessage(messages.Message):
    message = messages.StringField(1)
    code = messages.StringField(2)
    data = messages.StringField(3)


class SearchMessage(messages.Message):
    query = messages.StringField(1)


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


class FeedbackMessage(messages.Message):
    feedback_id = messages.StringField(1)
    author_uid = messages.StringField(2)
    rating = messages.StringField(3)
    comment = messages.StringField(4)
    item_id = messages.StringField(5)
    seller_uid = messages.StringField(6)
    transaction = messages.StringField(7)
    created_at = messages.StringField(8)


class FeedbackMessageCollection(messages.Message):
    message = messages.StringField(1)
    code = messages.StringField(2)
    data = messages.MessageField(FeedbackMessage, 3, repeated=True)