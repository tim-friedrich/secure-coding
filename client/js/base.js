/**
 * @fileoverview
 * Provides methods for the Hello Endpoints sample UI and interaction with the
 * Hello Endpoints API.
 */

/** google global namespace for Google projects. */
var google = google || {};

/** appengine namespace for Google Developer Relations projects. */
google.appengine = google.appengine || {};

/** samples namespace for App Engine sample code. */
google.appengine.secure = google.appengine.secure || {};

/** hello namespace for this sample. */
google.appengine.secure.shop = google.appengine.secure.shop || {};

/**
 * Initializes the application.
 * @param {string} apiRoot Root of the API's path.
 */
google.appengine.secure.shop.init = function(apiRoot) {
  // Loads the OAuth and helloworld APIs asynchronously, and triggers login
  // when they have completed.
  var apisToLoad;
  var callback = function() {
    if (--apisToLoad == 0) {
      google.appengine.secure.shop.enableButtons();
      google.appengine.secure.shop.signin(true,
          google.appengine.secure.shop.userAuthed)
    }
  }

  apisToLoad = 2; // must match number of calls to gapi.client.load()
  gapi.client.load('hardcode', 'v1', callback, apiRoot);
  gapi.client.load('oauth2', 'v2', callback);
};

/**
 * Enables the button callbacks in the UI.
 */
google.appengine.secure.shop.enableButtons = function() {
/*  var getItem = document.querySelector('#getGreeting');
  getItem.addEventListener('click', function(e) {
    google.appengine.secure.shop.getItem(
        document.querySelector('#id').value);
  });
*/
  var listItems = document.querySelector('#listItems');
  listItems.addEventListener('click',
      google.appengine.secure.shop.listItems);

  var signinButton = document.querySelector('#signinButton');
  signinButton.addEventListener('click', google.appengine.secure.shop.auth);

};

/**
 * Prints a greeting to the greeting log.
 * param {Object} greeting Greeting to print.
 */

google.appengine.secure.shop.print = function(item) {
  var element = document.createElement('div');
  element.classList.add('row');
  element.innerHTML = item.message;
  document.querySelector('#outputLog').appendChild(element);
};

/**
 * Gets a numbered greeting via the API.
 * @param {string} id ID of the greeting.
 */
/*
google.appengine.secure.shop.getItem = function(id) {
  gapi.client.hardcode.items.getItem({'id': id}).execute(
      function(resp) {
        if (!resp.code) {
          google.appengine.secure.shop.print(resp);
        }
      });
};
*/
/**
 * Lists greetings via the API.
 */
google.appengine.secure.shop.listItems = function() {
  gapi.client.hardcode.items.listItems().execute(
      function(resp) {
        if (!resp.code) {
          resp.items = resp.items || [];
          for (var i = 0; i < resp.items.length; i++) {
            google.appengine.secure.shop.print(resp.items[i]);
          }
        }
      });
};

/**
 * Client ID of the application (from the APIs Console).
 * @type {string}
 */
google.appengine.secure.shop.CLIENT_ID =
    '142521807042.apps.googleusercontent.com';

google.appengine.secure.shop.LOCAL_CLIENT_ID =
    '142521807042-l2afethj1qsrj64hecteq6rdth0qngrm.apps.googleusercontent.com';

/**
 * Scopes used by the application.
 * @type {string}
 */
google.appengine.secure.shop.SCOPES =
    'https://www.googleapis.com/auth/userinfo.email';

/**
 * Handles the auth flow, with the given value for immediate mode.
 * @param {boolean} mode Whether or not to use immediate mode.
 * @param {Function} callback Callback to call on completion.
 */
google.appengine.secure.shop.signin = function(mode, callback) {
  gapi.auth.authorize({client_id: google.appengine.secure.shop.CLIENT_ID,
      scope: google.appengine.secure.shop.SCOPES, immediate: mode},
      callback);
  gapi.auth.authorize({client_id: google.appengine.secure.shop.LOCAL_CLIENT_ID,
      scope: google.appengine.secure.shop.SCOPES, immediate: mode},
      callback);
};

/**
 * Presents the user with the authorization popup.
 */
google.appengine.secure.shop.auth = function() {
  if (!google.appengine.secure.shop.signedIn) {
    google.appengine.secure.shop.signin(false,
        google.appengine.secure.shop.userAuthed);
  } else {
    google.appengine.secure.shop.signedIn = false;
    document.querySelector('#signinButton').textContent = 'Sign in';
    document.querySelector('#authedGreeting').disabled = true;
  }
};

/**
 * Whether or not the user is signed in.
 * @type {boolean}
 */
google.appengine.secure.shop.signedIn = false;

/**
 * Loads the application UI after the user has completed auth.
 */
google.appengine.secure.shop.userAuthed = function() {
  var request = gapi.client.oauth2.userinfo.get().execute(function(resp) {
    if (!resp.code) {
      google.appengine.secure.shop.signedIn = true;
      document.querySelector('#signinButton').textContent = 'Sign out';
      document.querySelector('#authedGreeting').disabled = false;
    }
  });
};