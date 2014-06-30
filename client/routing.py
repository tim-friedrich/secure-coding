import webapp2
import jinja2
import os


class IndexPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render({}))
        return self.response


class ItemsPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('pages/items/items.html')
        self.response.write(template.render({}))
        return self.response


class AddItemPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('pages/items/add.html')
        self.response.write(template.render({}))
        return self.response


class ItemPage(webapp2.RequestHandler):
    def get(self, item_id):
        template = JINJA_ENVIRONMENT.get_template('pages/items/show.html')
        self.response.write(template.render({"item_id": item_id}))
        return self.response


class ItemEditPage(webapp2.RequestHandler):
    def get(self, item_id):
        template = JINJA_ENVIRONMENT.get_template('pages/items/add.html')
        self.response.write(template.render({'item_id': item_id}))
        return self.response


class UserPage(webapp2.RequestHandler):
    def get(self, user_id):
        template = JINJA_ENVIRONMENT.get_template('pages/users/show.html')
        self.response.write(template.render({'user_id': user_id}))
        return self.response


class UserEditPage(webapp2.RequestHandler):
    def get(self, user_id):
        template = JINJA_ENVIRONMENT.get_template('pages/users/edit.html')
        self.response.write(template.render({'user_id': user_id}))
        return self.response


class myItemsPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('pages/items/myItems.html')
        self.response.write(template.render({}))
        return self.response


class AddCommPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('pages/comms/add.html')
        try:
            self.response.write(template.render({'item_id': self.request.GET['item']}))
        except KeyError:
            self.response.write(template.render({}))
        return self.response


class CommPage(webapp2.RequestHandler):
    def get(self, comm_id):
        template = JINJA_ENVIRONMENT.get_template('pages/comms/show.html')
        self.response.write(template.render({"comm_id": comm_id}))
        return self.response


class CommsPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('pages/comms/comms.html')
        self.response.write(template.render({}))
        return self.response

application = webapp2.WSGIApplication([
    ('/items/add', AddItemPage),
    ('/items/myItems', myItemsPage),
    ('/', IndexPage),
    ('/items', ItemsPage),
    ('/items/edit/(\d+)', ItemEditPage),
    ('/items/(\d+)', ItemPage),
    ('/users/(\d+)', UserPage),
    ('/users/edit/(\d+)', UserEditPage),
    ('/comms/add', AddCommPage),
    ('/comms/(\d+)', CommPage),
    ('/comms', CommsPage)
], debug=True)

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)