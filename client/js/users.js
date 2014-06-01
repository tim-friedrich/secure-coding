google.appengine.secure.shop.loadUser = function(){
    var request = {}

    gapi.client.hardcode.users.getUser({ id: $('#user').attr('data-id') }).execute(function(resp){
        $user = $('#user');
        if (resp.code == "OK"){
            user = resp.data[0];
            $content = $('#content');
            $content.find('#name').text(user.name);
            $content.find('#email').text(user.email);
            $content.find('#description').text(user.description);
            $content.find('#user-image').attr('href', user.image);
        }
    });
}