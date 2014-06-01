
from google.appengine.ext import endpoints
from google.appengine.ext import ndb
from messages import ItemMessage, ItemMessageCollection, UserMessage, \
    UserMessageCollection, CommMessage, CommMessageCollection

class Item(ndb.Model):    
    title = ndb.StringProperty(indexed=True)
    description = ndb.StringProperty(indexed=True)
    expiration = ndb.DateTimeProperty(indexed=False)
    price = ndb.StringProperty(indexed=True)
    owner = ndb.KeyProperty(kind="User")
    created_at = ndb.DateTimeProperty(auto_now_add=True)

    def to_message(self):
        return ItemMessage(
            title=self.title,
            description=self.description,
            expiration=str(self.expiration),
            price=self.price,
            owner=self.owner.get().to_message(),
            item_id=str(self.key.id()),
            created_at=str(self.created_at))

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
    created_at = ndb.DateTimeProperty(auto_now_add=True)

    def to_message(self):
        return UserMessage(
            user_id=str(self.key.id()),
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
        if endpoints.get_current_user() is not None:
            user = User.query(User.email == endpoints.get_current_user().email()).get()
            if user is not None:
                return user.key
            else:
                user = User(email=endpoints.get_current_user().email())
                return user.put()
        else:
            return False


class Comm(ndb.Model):
    subject = ndb.StringProperty(indexed=False)
    sender = ndb.KeyProperty(kind="User")
    #multiple receiver
    receiver = ndb.KeyProperty(kind="User", repeated=True)
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    content = ndb.StringProperty(indexed=False)
    item_id = ndb.StringProperty(indexed=False)
    item_title = ndb.StringProperty(indexed=False)
    price = ndb.StringProperty(indexed=False)
    created_at = ndb.DateTimeProperty(auto_now_add=True)

    def to_message(self):
        return CommMessage(
            subject=self.subject,
            sender=self.sender,
            #multiple receiver
            receiver=self.receiver,
            timestamp=self.timestamp,
            content=self.content,
            item_id=self.item_id,
            item_title=self.item_title,
            price=self.price,
            created_at=self.created_at)

    @classmethod
    def to_message_collection(Comm, comms):
        commMessages = []
        for comm in comms:
            commMessages.append(comm.to_message())

        return CommMessageCollection(
            code="OK",
            message="OK",
            data=commMessages)


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
    created_at = ndb.DateTimeProperty(auto_now_add=True)


class Feedback(ndb.Model):
    feedback_id = ndb.StringProperty(indexed=False)
    author = ndb.StringProperty(indexed=False)
    rating = ndb.StringProperty(indexed=False)
    comment = ndb.StringProperty(indexed=False)
    item_id = ndb.StringProperty(indexed=False)
    seller_uid = ndb.StringProperty(indexed=False)
    transaction_id = ndb.StringProperty(indexed=False)
    created_at = ndb.DateTimeProperty(auto_now_add=True)
