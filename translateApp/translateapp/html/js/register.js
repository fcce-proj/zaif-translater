$(function(){
  $(document).on('click','.edit-btn', function(arg1){
    var click_id_name =  arg1.target.id;
    var id_name_id = click_id_name.replace(/(-[a-z]{2})/g,'');
    var id_name_ja = click_id_name.replace(/([a-z]{2})/g,'ja');
    var id_name_en = click_id_name.replace(/([a-z]{2})/g,'en');
    var id_name_zh = click_id_name.replace(/([a-z]{2})/g,'zh');

    var td_ja = $("#"+ id_name_ja).text();
    var td_en = $("#"+ id_name_en).text();
    var td_zh = $("#"+ id_name_zh).text();


    $(':hidden[name="edit_id"]').val(id_name_id);
    $(':text[name="edit_ja"]').val(td_ja);
    $(':text[name="edit_en"]').val(td_en);
    $(':text[name="edit_zh"]').val(td_zh);

    $('#modal-content').show();
    $('#modal-overlay').show();
  });

  $(document).on('click','#modal-close-btn, #modal-overlay', function(){
    $('#modal-content').hide();
    $('#modal-overlay').hide();
  });

  centeringModal()
  function centeringModal(){
  	var w = $(window).width();
  	var h = $(window).height();
  	// var cw = $("#modal-content").outerWidth({margin:true});
  	// var ch = $("#modal-content").outerHeight({margin:true});
  	var pxleft = w / 2 - 347;
  	var pxtop = h / 2- 184;

  	$("#modal-content").css({"left": pxleft, "top": pxtop});
  };

  // 登録のajax
  $("#register_submit").on('click', function(){
    var params = {'ja': $('#register_ja').val(), 'en': $('#register_en').val(), 'zh': $('#register_zh').val()};
    var deferred = new $.Deferred();

    if ($('#register_ja').val() == '' || $('#register_en').val() == '' || $('#register_zh').val() == '' ) {
      alert("フィールドに入力して下さい。");
      return false;
    }

     $.ajax({
       type: 'POST',
       url: 'register',
       data: params,
     }).done(function (data) {
        // location.reload();
        OpenErrorMsg(data.register_flag, data.key);
     }).fail(function () {
       alert('データを送信できません');
     }).always(function () {
       deferred.resolve();
     });
     return deferred;
  });

  // 編集のajax
  $("#edit_submit").on('click', function(){
    var params = {'edit_id': $('#edit_id').val(), 'edit_ja': $('#edit_ja').val(), 'edit_en': $('#edit_en').val(), 'edit_zh': $('#edit_zh').val()};
    var deferred = new $.Deferred();

    if ($('#edit_ja').val() == '' || $('#edit_en').val() == '' || $('#edit_zh').val() == '' ) {
      alert("フィールドに入力して下さい。");
      return false;
    }

     $.ajax({
       type: 'POST',
       url: 'edit',
       data: params,
       dataType: 'json'
     }).done(function (data) {
       location.reload();
     }).fail(function () {
       alert('データを送信できません');
     }).always(function () {
       deferred.resolve();
     });
     return deferred;
  });

});

function checkForm1(){
  if(document.form1.search.value == ""){
      alert("フィールドに入力して下さい");
      return false;
    } else {
      return true;
    }
  };

function checkForm2(){
  if(document.form2.csv.value == ""){
      alert("ファイルを添付してください");
      return false;
    } else {
      return true;
    }
  };

function OpenErrorMsg(flag, key){
  if (flag == true){
    $('.success-board').show();
    $('.failed-board').hide();
    $('.success-board').prepend('<p style="font-size:30px; color:#ffffff; text-align:center; padding-top:5px;">success: '+ key +' を登録しました</p>');
    setTimeout(function(){
      $('.success-board').fadeOut();
      setTimeout("location.reload()", 200);
    },2000);
  } else {
    $('.failed-board').show();
    $('.success-board').hide();
    $('.failed-board').prepend('<p class="failed-msg" style="font-size:30px; color:#ffffff; text-align:center; padding-top:5px; ">failed: '+ key +' のkeyはすでに存在しています</p>');
    setTimeout(function(){
      $('.failed-board').fadeOut();
      $('.failed-msg').fadeOut();
    },2000);
  }
};
