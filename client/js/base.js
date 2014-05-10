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
    }
  }

  apisToLoad = 1; // must match number of calls to gapi.client.load()
  gapi.client.load('hardcode', 'v1', callback, apiRoot);
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