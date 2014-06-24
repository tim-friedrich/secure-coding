"""Hello World API implemented using Google Cloud Endpoints.

Defined here are the ProtoRPC messages needed to define Schemas for methods
as well as those methods defined in an API.
"""
from datetime import date, datetime
import time

import endpoints
from google.appengine.api.datastore_errors import BadValueError
from google.appengine.ext import endpoints
from google.appengine.ext import ndb
from protorpc import messages
from protorpc import message_types
from protorpc import remote
from messages import UserMessageCollection, UserMessage, ItemMessage, ItemMessageCollection, \
    BaseMessage, CommMessage, CommMessageCollection
from models import User, Item, Comm
from backend.messages import SearchMessage, FeedbackMessage, FeedbackMessageCollection

package = 'SecureCoding'

WEB_CLIENT_ID = '142521807042.apps.googleusercontent.com'
LOCAL_CLIENT_ID = '142521807042-f6qni9r0isipad8nldolobfvtdm64j58.apps.googleusercontent.com'
ANDROID_AUDIENCE = WEB_CLIENT_ID


hardcode = endpoints.api(name='hardcode', version='v1',
                        allowed_client_ids=[WEB_CLIENT_ID, LOCAL_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID],
                        audiences=[ANDROID_AUDIENCE],
                        scopes=[endpoints.EMAIL_SCOPE])

def check_signed_in():
    current_user = User.get_current_user()

    if not current_user:
        raise endpoints.UnauthorizedException('Invalid token.')
    else:
        return current_user

@hardcode.api_class(resource_name='items', path="items")
class Items(remote.Service):

    ##Item api
    ITEMS_RESOURCE = endpoints.ResourceContainer(
        ItemMessage)

    ITEMS_COLLECTION_RESOURCE = endpoints.ResourceContainer(
        ItemMessageCollection)

    @endpoints.method(ITEMS_RESOURCE, BaseMessage,
                      path='items/add', http_method='POST',
                      name='addItem')
    def add_item_post(self, request):
        check_signed_in()
        try:
            item = Item(
                title=request.title,
                description=request.description,
                expiration=datetime.strptime(request.expiration, "%m/%d/%Y"),
                price=request.price,
                owner=User.get_current_user()
            )
            key = item.put()
            return BaseMessage(message="OK", code="OK", data=str(key.id()))
        except BadValueError as e:
            return BaseMessage(message= e.message, code="ERROR", data=e.message)

    ID_RESOURCE = endpoints.ResourceContainer(
        message_types.VoidMessage,
        id=messages.IntegerField(1, variant=messages.Variant.INT32))

    @endpoints.method(ID_RESOURCE, ItemMessageCollection,
                      path='items/{id}', http_method='GET',
                      name='getItem')
    def items_get(self, request):
        item = Item.get_by_id(request.id)
        #add filter for expiration
        if item:
            return Item.to_message_collection([item])
        else:
            raise endpoints.NotFoundException('Item %s not found.' %
                                              (request.id,))

    @endpoints.method(message_types.VoidMessage, ItemMessageCollection,
                      path='items', http_method='GET',
                      name='listItems')
    def list_items_get(self, request):
        #missing filter for expired items
        return Item.to_message_collection(Item.query())

    @endpoints.method(ID_RESOURCE, BaseMessage,
                      path='items/del/{id}', http_method='POST',
                      name='delItem')
    def del_item_post(self, request):
        user = check_signed_in()

        item = Item.get_by_id(request.id)
        if item.owner != User.get_current_user():
            return BaseMessage(message="Missing permissions",
                               code="ERROR",
                               data="You are not authorized to delete the Item.")
        if item:
            item.key.delete()
            return BaseMessage(message="OK", code="OK", data="Item successful deleted")
        else:
            raise endpoints.NotFoundException('Item %s not found.' %
                                              (request.id,))

    @endpoints.method(ITEMS_RESOURCE, BaseMessage,
                      path='items/mod', http_method='POST',
                      name='modItem')
    def mod_item_post(self, request):
        user = check_signed_in()
        item = Item.get_by_id(request.item_id)
        if item.owner == user:
            item.description = request.description
            item.expiration = request.expiration
            item.price = request.price
            item.title = request.title
            item.put()
            return BaseMessage(message="OK", code="OK", data=str(item.key.id()))
        else:
            raise endpoints.UnauthorizedException('')


@hardcode.api_class(resource_name='users', path="users")
class Users(remote.Service):
    ##Item api
    USERS_RESOURCE = endpoints.ResourceContainer(
            UserMessage)

    USERS_COLLECTION_RESOURCE = endpoints.ResourceContainer(
            UserMessageCollection)


    @endpoints.method(USERS_RESOURCE, BaseMessage,
                      path='user/add', http_method='POST',
                      name='addUsers')
    def add_user_post(self, request):
        check_signed_in()
        #check if email already exists
        user = User(
            email=endpoints.get_current_user().email(),
            name=request.name,
            description=request.description,
            image_url=request.image_url,
            tag=request.tag,
            disabled=request.disabled)
        key = user.put()
        return BaseMessage(message="OK", code="OK", data=str(key.id()))

    ID_RESOURCE = endpoints.ResourceContainer(
        message_types.VoidMessage,
        id=messages.IntegerField(1, variant=messages.Variant.INT32))

    @endpoints.method(ID_RESOURCE, UserMessageCollection,
                      path='user/{id}', http_method='GET',
                      name='getUser')
    def users_get(self, request):
        #nur user selbst und admin?
        user = User.get_by_id(request.id)
        if user:
            return User.to_message_collection([user])
        else:
            raise endpoints.NotFoundException('Item %s not found.' %
                                              (request.id,))

    @endpoints.method(message_types.VoidMessage, UserMessageCollection,
                      path='users', http_method='GET',
                      name='listUsers')
    def list_users_get(self, request):
        check_signed_in()
        return User.to_message_collection(User.query())

    @endpoints.method(ID_RESOURCE, BaseMessage,
                      path='user/del/{id}', http_method='POST',
                      name='delUser')
    def del_user_post(self, request):
        #delete Users Items?
        check_signed_in()
        user = User.get_by_id(request.id)

        if user and user == User.query(User.email == endpoints.get_current_user().email()).get():
            user.key.delete()
            return BaseMessage(message="OK", code="OK", data="User deleted")
        else:
            raise endpoints.NotFoundException('Item %s not found.' %
                                              (request.id,))

    @endpoints.method(USERS_RESOURCE, BaseMessage,
                      path='user/mod', http_method='POST',
                      name='modUser')
    def mod_user_post(self, request):
        user = check_signed_in().get()
        if user.key.id() == long(request.user_id):
            user.name = request.name
            user.description = request.description
            user.image_url = request.image_url
            user.put()

            return BaseMessage(message="OK", code="OK", data=str(user.key.id()))
        else:
            raise endpoints.UnauthorizedException('')

@hardcode.api_class(resource_name='search', path="search")
class Search(remote.Service):
    SEARCH_RESOURCE = endpoints.ResourceContainer(
            SearchMessage)
    @endpoints.method(SEARCH_RESOURCE, ItemMessageCollection,
                      path='search/query', http_method='GET',
                      name='query')
    def query_get(self, request):
        items = []
        for item in Item.query():
            if((request.query.lower() in item.title.lower() or
                    request.query.lower() in item.description.lower() or
                    request.query in item.price) and
                    item.expiration >= date.today()):
                items.append(item)

        return Item.to_message_collection(items)



@hardcode.api_class(resource_name='comms', path="comms")
class Comms(remote.Service):
    ##Item api
    COMMS_RESOURCE = endpoints.ResourceContainer(
            CommMessage)

    COMMS_COLLECTION_RESOURCE = endpoints.ResourceContainer(
            CommMessageCollection)

    @endpoints.method(COMMS_RESOURCE, BaseMessage,
                      path='comm/add', http_method='POST',
                      name='addComm')
    def add_comm_post(self, request):
        user = check_signed_in()
        item = Item.get_by_id(long(request.item_id))
        try:
            comm = Comm(
                subject=request.subject,
                sender=user.id(),
                receiver=request.receiver.split(';'),
                content=request.content,
                item_id=item,
                item_title=item.title,
                price=item.price)
            key = comm.put()
            return BaseMessage(message="OK", code="OK", data=str(key.id()))
        except Exception as e:
            return BaseMessage(message=e.message, code="ERROR", data=e.message)

    ID_RESOURCE = endpoints.ResourceContainer(
        message_types.VoidMessage,
        id=messages.IntegerField(1, variant=messages.Variant.INT32))

    @endpoints.method(ID_RESOURCE, CommMessageCollection,
                      path='comm/{id}', http_method='GET',
                      name='getComm')
    def comm_get(self, request):
        user = check_signed_in()
        comm = Comm.get_by_id(request.id)
        #multiple receivers...

        if comm and (user == comm.sender or user == comm.receiver):
            return Comm.to_message_collection([comm])
        else:
            raise endpoints.NotFoundException('Item %s not found.' %
                                                  (request.id,))

    @endpoints.method(message_types.VoidMessage, CommMessageCollection,
                      path='comms', http_method='GET',
                      name='listComm')
    def list_comms_get(self, request):
        #missing filter
        return Comm.to_message_collection(Comm.query())

    @endpoints.method(ID_RESOURCE, BaseMessage,
                      path='comm/del/{id}', http_method='POST',
                      name='delComm')
    def del_comm_post(self, request):
        #delete Users Items?
        user = check_signed_in()
        comm = Comm.get_by_id(request.id)

        if comm and comm.sender == User.query(User.email == endpoints.get_current_user()).get():
            comm.delete()
            return BaseMessage(message="OK", code="OK", data="User deleted")
        else:
            raise endpoints.NotFoundException('Item %s not found.' %
                                              (request.id,))


@hardcode.api_class(resource_name='feedbacks', path="feedbacks")
class Feedback(remote.Service):
    ##Item api
    FEEDBACK_RESOURCE = endpoints.ResourceContainer(
            FeedbackMessage)

    FEEDBACK_COLLECTION_RESOURCE = endpoints.ResourceContainer(
            FeedbackMessageCollection)

    @endpoints.method(FEEDBACK_RESOURCE, BaseMessage,
                      path='feedbacks/add', http_method='POST',
                      name='addFeedback')
    def add_feedback_post(self, request):
        check_signed_in()
        feedback = Feedback()
        key = feedback.put()
        return BaseMessage(message="OK", code="OK", data=str(key.id()))

    ID_RESOURCE = endpoints.ResourceContainer(
        message_types.VoidMessage,
        id=messages.IntegerField(1, variant=messages.Variant.INT32))

    @endpoints.method(ID_RESOURCE, FeedbackMessageCollection,
                      path='feedbacks/{id}', http_method='GET',
                      name='getFeedback')
    def feedback_get(self, request):
        user = check_signed_in()
        feedback = Feedback.get_by_id(request.id)

        return Feedback.to_message(feedback)

    @endpoints.method(message_types.VoidMessage, FeedbackMessageCollection,
                      path='feedbacks', http_method='GET',
                      name='listFeedbacks')
    def list_feedbacks_get(self, request):
        #missing filter
        return Feedback.to_message_collection(Feedback.query())

    @endpoints.method(ID_RESOURCE, BaseMessage,
                      path='feedbacks/del/{id}', http_method='POST',
                      name='delFeedback')
    def del_feedback_post(self, request):
        #delete Users Items?
        user = check_signed_in()
        feedback = Feedback.get_by_id(request.id)

        if feedback and feedback.author == User.query(User.email == endpoints.get_current_user()).get():
            feedback.delete()
            return BaseMessage(message="OK", code="OK", data="Feedback deleted")
        else:
            raise endpoints.NotFoundException('Feedback %s not found.' %
                                              (request.id,))


APPLICATION = endpoints.api_server([hardcode])