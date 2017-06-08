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

  // centeringModalLogin()
  function centeringModalLogin(){
    	var w = $(window).width();
    	var h = $(window).height();
    	// var cw = $("#modal-content").outerWidth({margin:true});
    	// var ch = $("#modal-content").outerHeight({margin:true});
    	var pxleft = w / 2-150;
    	var pxtop = h / 2-150;

    	$("#login-formt").css({"left": pxleft, "top": pxtop});
  };

})