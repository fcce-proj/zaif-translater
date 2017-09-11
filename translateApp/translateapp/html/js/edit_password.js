$(function(){
  $("#again_new_password").change(function(){
    var new_password = $('#new_password').val();
    var again_new_password = $('#again_new_password').val();

    if (new_password != again_new_password) {
      $("#password_message").text("パスワードが一致しません。");
      $("#password_message").show();
    } else {
      $("#password_message").hide();
    }
  });

  $("#submit").on('click', function(){
  var params = {'password':$('#password').val(), 'new_password':$('#new_password').val()};
  var deferred = new $.Deferred();

   $.ajax({
       type: 'POST',
       url: 'edit_password',
       data: params,
       dataType: 'json'
   }).done(function (data) {
     var result = data.result;
      var message = data.message;
      console.log(message);
      $('#result_message').text(message);
      $('#result_message').show();
      if (result) {
        $('#password, #new_password, #again_new_password').val("");
      }
   }).fail(function () {
      alert('パスワード変更に失敗しました。(ajax error)');
   }).always(function () {
       deferred.resolve();
   });
   return deferred.promise();
  });
})
