
define(['jquery', 'utils'], function ($, utils) {
    "use strict";
    var token = 1;
    var base_url = window.jhdata.base_url;
    var prefix = window.jhdata.prefix;
    //var data = {'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImNocmlzIiwicGFzc3dvcmQiOjEyM30.cIZv4gl8AppP46Uw5J-5WOCq6riptU9A32kwh24Ufcg'}
    var data = {'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InJhZHUiLCJwYXNzd29yZCI6MTIzNH0.fLTcvWJ6W3C2aEEw6bDA4giFMF_kRmELUqYDBn6-D-c'}
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
            }
        }
   });
});