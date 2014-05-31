

google.appengine.secure.shop.enableButtons = function() {

  var signinButton = document.querySelector('#signinButton');
  signinButton.addEventListener('click', google.appengine.secure.shop.auth);

};