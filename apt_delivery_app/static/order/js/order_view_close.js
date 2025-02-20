$(document).ready(function() {
  $('.close_all, .view_all').click( function(e){
    switch (true) {
      case $(this).hasClass('close_all'):
        $(this).addClass("view_all").removeClass('close_all').html('Показать все')
        $(".accordion-button").addClass('collapsed').attr('aria-expanded', 'false');
        $(".accordion-collapse").removeClass('show')
        break;
      case $(this).hasClass('view_all'):
        $(this).addClass("close_all").removeClass('view_all').html('Скрыть все')
        $(".accordion-button").removeClass('collapsed').attr('aria-expanded', 'true');
        $(".accordion-collapse").addClass('show')
        break;

      default:
       
        break;
    }
  })
})