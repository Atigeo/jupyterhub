
define(['jquery', 'utils'], function ($, utils) {
    "use strict";
    var token = 1;
    var base_url = window.jhdata.base_url;
    var prefix = window.jhdata.prefix;
    var data = {'token':
    'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE0NTk0Mjg0MjMzNjYsInN1YiI6ImFkbWluQHhwYXR0ZXJucy5jb20iLCJleHAiOjE0NTk0MzAyMjMzNjYsImFkbWluIjoidHJ1ZSIsImlzcyI6InhQYXR0ZXJucyJ9.vrSfR7ZFT4pmklitbHeciMQJQ7auWOeBFqIuiKXIZL4'
    };

    console.log(base_url);
    console.log(prefix);
    console.log(data);
   $('#login_btn').click(function(){
        var url = utils.url_path_join(prefix, base_url, 'login') + '?next=';
        $.post(url, data, success)
            .fail(function(e){
                console.log(e);
            });
        function success(html){
            if(html.indexOf('Sign in') == -1){
                window.location.reload();
            }
            else{
                var newDoc = document.open('text/html','replace');
                newDoc.write(html);
                newDoc.close();
                setTimeout(function(){window.location.reload();}, 750);
            }
        }
   });
});