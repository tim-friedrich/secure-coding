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
        console.log("API ready");
        google.appengine.secure.shop.signin(true, google.appengine.secure.shop.userAuthed);
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
    console.log("Signing in...");
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
            console.log("User signed in");
            google.appengine.secure.shop.signedIn = true;
            google.appengine.secure.shop.setCurrentUser(resp.email);
        } else {
            console.log("Sign in failed");
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
                    console.log("Current user set:");
                    console.log(user);

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

// Navigation
google.appengine.secure.shop.renderLoggedInNav = function () {
    $('nav').find('#currentUserNav').attr(
        'href',
        '/users/'+google.appengine.secure.shop.currentUser.user_id
    );
    $('nav').find('#userSettings').attr(
        'href',
        '/users/edit/'+google.appengine.secure.shop.currentUser.user_id
    );

    $('#signinButton').html("Logout");

    if (google.appengine.secure.shop.currentUser.image_url != null) {
        $('nav').find('#user_image_nav').attr('src', google.appengine.secure.shop.currentUser.image_url);
    } else {
        $('nav').find('#user_image_nav').attr('src', '../media/user_default.jpg');
    }
    $('nav').find('#user_image_nav').show();
    /*
    $('nav').find('#user_image_nav').addEventListener('click', new function () {
        document.location = '/users/'+google.appengine.secure.shop.currentUser.user_id;
    });
    */
    $('#user_image_nav')[0].addEventListener('click', function () {
        document.location = '/users/'+google.appengine.secure.shop.currentUser.user_id;
    });
}

google.appengine.secure.shop.renderNav = function () {
        console.log("Rendering navigation");
    var signinButton = document.querySelector('#signinButton');
    signinButton.addEventListener('click', google.appengine.secure.shop.auth);

    $('nav').find('#user_image_nav').hide();
}


// Loading dialog
google.appengine.secure.shop.showLoadingDialog = function (title) {
    if (title == null) {
        title = "Loading";
    }
    document.getElementById("content").style.opacity = "0.1";
    var dialog = document.getElementById("loading");
    dialog.style.top = "50%";
    dialog.style.opacity = "1";
    dialog.children[0].innerHTML = title;
}

google.appengine.secure.shop.hideLoadingDialog = function () {
    document.getElementById("content").style.opacity = "1";
    var dialog = document.getElementById("loading");
    dialog.style.top = "-200px";
    dialog.style.opacity = "0";
}

// Readability
google.appengine.secure.shop.getReadableUserName = function (user) {
    //console.log(user);
    if (user.name != null) {
        return user.name;
    } else if (user.email.indexOf("@") != -1) {
        return user.email.substr(0, user.email.indexOf("@"));
    } else {
        return user.email;
    }
}

google.appengine.secure.shop.getReadableDate = function (dateString) {
    try {
        var date = new Date(dateString).getTime();
        var now = new Date().getTime();

        // Difference in seconds
        var dif = Math.round((now - date) / 1000);
        if (dif < 0) {
            dif = dif * (-1);
        }

        var dif_days = Math.round(dif / 60 / 60 / 24);
        var dif_hours = Math.round((dif / 60 / 60) - (dif_days * 24));
        var dif_minutes = Math.round((dif / 60) - (dif_days * 24) - (dif_hours * 60));

        var result;

        if (now < date) {
            if (dif_days > 1) {
                result = "In " + dif_days + " days";
            } else if (dif_days > 0) {
                result = "Tomorrow";
            } else {
                if (dif_hours > 1) {
                    result = "In " + dif_hours + " hours";
                } else if (dif_hours > 0) {
                    result = "In " + dif_hours + " hour";
                } else {
                    if (dif_minutes > 1) {
                        result = "In " + dif_hours + " minutes";
                    } else {
                        result = "Now";
                    }
                }
            }
        } else {
            if (dif_days > 1) {
                result = dif_days + " days ago";
            } else if (dif_days > 0) {
                result = "Yesterday";
            } else {
                if (dif_hours > 1) {
                    result = dif_hours + " hours ago";
                } else if (dif_hours > 0) {
                    result = dif_hours + " hour ago";
                } else {
                    if (dif_minutes > 1) {
                        result = dif_minutes + " minutes ago";
                    } else {
                        result = "Now";
                    }
                }
            }
        }

        return result;
    } catch (ex) {
        return dateString;
    }
}