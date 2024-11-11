$("form.ajaxForm").submit((e) => {
  e.preventDefault();
  return false;
});
$(".checkFormBtn").click(() => {
  if (!$("form.ajaxForm").get(0).checkValidity()) return;
  $("form.ajaxForm .border-danger").removeClass("border-danger");
  $("form.ajaxForm .errorlist").remove();
  $.post(window.location.pathname, $("form.ajaxForm").serialize(), (data) => {
    //console.log(data);
    Object.keys(data).forEach((key) => {
      //console.log(key);
      if (data[key] == "../orders.php") {
        $.get("cart_change.php?type=empty", {}, (res) => {
          window.location.replace(data[key]);
        });
      } else if (key == "is_valid") {
        window.location.replace(data[key]);
      }
      $("input[name=" + key + "]")
        .addClass("border-danger")
        .before($('<div class="errorlist"/>').html(data[key]));
    });
  });
});
//
