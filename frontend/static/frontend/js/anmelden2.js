$(function() {
  var $iban = $('#id_iban')
  var $feedback = $('<div class="form-control-feedback">')
  $feedback.text('Ungültige IBAN')
  
  $iban.on('keydown change', function() {
    if(!IBAN.isValid($iban.val())) {
      $iban.parent().addClass("has-danger")
      $iban.parent().append($feedback)
    }else{
      $iban.parent().removeClass("has-danger")
      $feedback.remove()
    }
  })
})
