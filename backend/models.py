
from google.appengine.ext import endpoints
from google.appengine.ext import ndb
from messages import ItemMessage, ItemMessageCollection, UserMessage, UserMessageCollection

class Item(ndb.Model):    
    title = ndb.StringProperty(indexed=False)
    description = ndb.StringProperty(indexed=False)
    expiration = ndb.DateTimeProperty(indexed=False)
    price = ndb.StringProperty(indexed=False)
    owner = ndb.KeyProperty(kind="User")
    created_at = ndb.DateTimeProperty(auto_now_add=True)

    def to_message(self):
        return ItemMessage(
            title=self.title,
            description=self.description,
            expiration=self.expiration,
            price=self.price,
            owner=self.owner.to_message(),
            item_id=str(self.key.id()))

    @classmethod
    def to_message_collection(Item, items):
        itemMessages = []
        for item in items:
            itemMessages.append(item.to_message())

        return ItemMessageCollection(
            code="OK",
            message="OK",
            data=itemMessages)


class User(ndb.Model):
    email = ndb.StringProperty(indexed=True)
    name = ndb.StringProperty(indexed=False)
    description = ndb.StringProperty(indexed=False)
    image_url = ndb.StringProperty(indexed=False)
    tag = ndb.StringProperty(indexed=False)
    disabled = ndb.BooleanProperty(indexed=False)

    def to_message(self):
        return UserMessage(
            email=self.email,
            name=self.name,
            description=self.description,
            image_url=self.image_url,
            tag=self.tag,
            disabled=self.disabled)

    @classmethod
    def to_message_collection(Item, users):
        userMessages = []
        for user in users:
            userMessages.append(user.to_message())

        return UserMessageCollection(
            code="OK",
            message="OK",
            data=userMessages)

    @classmethod
    def get_current_user(self):
        return User.query(User.email == endpoints.get_current_user().email()).get().key


class Comm(ndb.Model):
    subject = ndb.StringProperty(indexed=False)
    sender = ndb.StringProperty(indexed=False)
    receiver = ndb.StringProperty(indexed=False)
    timestamp = ndb.StringProperty(indexed=False)
    content = ndb.StringProperty(indexed=False)
    item_id = ndb.StringProperty(indexed=False)
    item_title = ndb.StringProperty(indexed=False)
    price = ndb.StringProperty(indexed=False)


class Transaction(ndb.Model):
    closed = ndb.StringProperty(indexed=False)
    buyer_confirmation = ndb.StringProperty(indexed=False)
    seller_confirmation = ndb.StringProperty(indexed=False)
    seller = ndb.StringProperty(indexed=False)
    item_id = ndb.StringProperty(indexed=False)
    price = ndb.StringProperty(indexed=False)
    item_title = ndb.StringProperty(indexed=False)
    transaction_id = ndb.StringProperty(indexed=False)
    feedback_item = ndb.StringProperty(indexed=False)
    feedback_seller = ndb.StringProperty(indexed=False)


class Feedback(ndb.Model):
    feedback_id = ndb.StringProperty(indexed=False)
    author = ndb.StringProperty(indexed=False)
    rating = ndb.StringProperty(indexed=False)
    comment = ndb.StringProperty(indexed=False)
    item_id = ndb.StringProperty(indexed=False)
    seller_uid = ndb.StringProperty(indexed=False)
    transaction_id = ndb.StringProperty(indexed=False)

