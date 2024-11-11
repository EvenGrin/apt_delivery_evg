$(document).ready(function () {
  $(document).on("click","#nav a",  function (ev) {
    ev.preventDefault();
    $.ajax({
      url: "./php/ajax/ajax_pagination.php",
      method: "GET",
      data: {
        filter: $(this).data("href"),
      },
      success: (res) => {
        $("#nav a").removeClass("disabled");
        $(this).addClass("disabled");
        $("#card_inner").html(res);
        $("table").html(res);
      },
    });
  });
});
