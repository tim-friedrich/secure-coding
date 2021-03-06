/**
 * @fileoverview
 * Provides methods for the Hello Endpoints sample UI and interaction with the
 * Hello Endpoints API.
 */

/** google global namespace for Google projects. */
var google = google || {};

/** appengine namespace for Google Developer Relations projects. */
google.appengine = google.appengine || {};

google.appengine.secure = google.appengine.secure || {};

google.appengine.secure.shop = google.appengine.secure.shop || {};

google.appengine.secure.shop.current_user  = {}
/**
 * Initializes the application.
 * @param {string} apiRoot Root of the API's path.
 */
var initCallback;
google.appengine.secure.shop.init = function(apiRoot, callback) {
  // Loads the OAuth and helloworld APIs asynchronously, and triggers login
  // when they have completed.
  var apisToLoad;
  initCallback = callback;
  var api_ready = function() {
    if (--apisToLoad == 0) {
        google.appengine.secure.shop.signin(true,
            google.appengine.secure.shop.userAuthed);
        google.appengine.secure.shop.renderNav();
        }
  }


  apisToLoad = 2; // must match number of calls to gapi.client.load()
  gapi.client.load('hardcode', 'v1', api_ready, apiRoot);
  gapi.client.load('oauth2', 'v2', api_ready);
};

/**
 * Client ID of the application (from the APIs Console).
 * @type {string}
 */
google.appengine.secure.shop.CLIENT_ID =
    '142521807042.apps.googleusercontent.com';

google.appengine.secure.shop.LOCAL_CLIENT_ID =
    '142521807042-f6qni9r0isipad8nldolobfvtdm64j58.apps.googleusercontent.com';

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
google.appengine.secure.shop.userAuthed = function(e) {
    var request = gapi.client.oauth2.userinfo.get().execute(function(resp) {
        if (!resp.code) {
            google.appengine.secure.shop.signedIn = true;
            google.appengine.secure.shop.setCurrentUser(resp.email);
        }
        else{
            initCallback();
        }
    });
};


google.appengine.secure.shop.setCurrentUser = function (email){
    gapi.client.hardcode.users.listUsers().execute(
        function(resp) {
            if (resp.code == 'OK') {
              resp.data = resp.data || [];
              for(index in resp.data){
                  user = resp.data[index]
                  if(user.email == email){
                    google.appengine.secure.shop.currentUser = user;
                    google.appengine.secure.shop.renderLoggedInNav();
                    initCallback();
                    break;
                  }
              }
            }
        }
    );
}

google.appengine.secure.shop.renderLoggedInNav = function () {
    $('nav').find('#currentUserNav').attr(
        'href',
        '/users/'+google.appengine.secure.shop.currentUser.user_id
    );
    $('nav').find('#userSettings').attr(
        'href',
        '/users/edit/'+google.appengine.secure.shop.currentUser.user_id
    );

}

google.appengine.secure.shop.renderNav = function () {
    var signinButton = document.querySelector('#signinButton');
    signinButton.addEventListener('click', google.appengine.secure.shop.auth);
}

