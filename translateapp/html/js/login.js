$(function(){
  $("#submit").on('click', function(){
  var params = {'name': $('#name').val(), 'password':$('#password').val()};
  var deferred = new $.Deferred();

   $.ajax({
       type: 'POST',
       url: 'login',
       data: params,
       dataType: 'json'
   }).done(function (result) {
      location.href = result.query;
   }).fail(function () {
      alert('名前または、パスワードが違います。');
   }).always(function () {
       deferred.resolve();
   });
   return deferred;
  });
})
