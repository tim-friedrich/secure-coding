google.appengine.secure.shop.loadUser = function(){
    var request = {}
    gapi.client.hardcode.users.getUser({ id: $('#user').attr('data-id') }).execute(function(resp){
        $user = $('#user');
        if (resp.code == "OK"){
            user = resp.data[0];
            $content = $('#content');

            if (user.name != null) {
                $content.find('#name').text(user.name);
            } else {
                $content.find('#name').text("Unknown");
            }
            if (user.email != null) {
                $content.find('#email').text(user.email);
            } else {
                $content.find('#email').text("Unknown");
            }
            if (user.description != null) {
                $content.find('#description').text(user.description);
            } else {
                $content.find('#description').text("Not available");
            }
            if (user.image_url != null) {
                $content.find('#user_image').attr('src', user.image_url);
            } else {
                $content.find('#user_image').attr('src', '../media/user_default.jpg');
            }
        }
        google.appengine.secure.shop.hideLoadingDialog();
    });
}

google.appengine.secure.shop.initSettingsPage = function(){
    gapi.client.hardcode.users.getUser({ id: $('#user').attr('data-id') }).execute(function(resp){
        $user = $('#user');
        if (resp.code == "OK"){
            user = resp.data[0];
            $content = $('#content');
            $content.find('#user_name').val(user.name);
            $content.find('#user_description').val(user.description);
            $content.find('#user_image_input').val(user.image_url);
            google.appengine.secure.shop.hideLoadingDialog();
        }
    });

    $('#submit_button').on('click', function(event){
        event.preventDefault();
        gapi.client.hardcode.users.modUser(
            {
                'name': $('form').find('#user_name').val(),
                'user_id': $('#user').attr('data-id'),
                'description': $('form').find('#user_description').val(),
                'image_url': $('form').find('#user_image_input').val()
            }
        ).execute(function(resp){
                if(resp.code != "OK"){
                    alert("An Error has occurred while adding the item. The request returned with code: "+resp.code+" "+resp.message)
                }
                else{
                    window.location.replace('/users/'+$('#user').attr('data-id'))
                }
            });
        return false;
    });
}