$(document).ready(function () {
  function cart_add(id) {
    return (
      '<button class="btn btn-primary cart_add" data-id="' + id + '">+</button>'
    );
  }
  function cart_in(id) {
    return (
      '<button class="btn btn-primary cart_add ms-auto" data-id="' +
      id +
      '">В корзину</button>'
    );
  }
  function cart_sub(id) {
    return (
      '<button class="btn btn-primary cart_sub" data-id="' + id + '">-</button>'
    );
  }
  function cart_remove(id) {
    return (
      '<button class="btn btn-danger cart_remove me-auto" data-id="' +
      id +
      '">Убрать</button>'
    );
  }
  function span(data) {
    return "<span>" + data + "</span>";
  }
  $(document).on("click", ".cart_add", (e) => {
    let $obj = $(e.currentTarget),
      id = $obj.data("id");
    $.get("cart_change.php?type=add&id=" + id, {}, (data) => {
      $obj
        .parent()
        .html(cart_remove(id) + cart_sub(id) + span(data) + cart_add(id));
    });
  });
  $(document).on("click", ".cart_sub", (e) => {
    let $obj = $(e.currentTarget),
      id = $obj.data("id");
    $.get("cart_change.php?type=sub&id=" + $obj.data("id"), {}, (data) => {
      $obj
        .parent()
        .html(cart_remove(id) + cart_sub(id) + span(data) + cart_add(id));
    });
  });

  $(document).on("click", ".cart_remove", (e) => {
    let $obj = $(e.currentTarget),
      id = $obj.data("id");
    $.get("cart_change.php?type=remove&id=" + $obj.data("id"), {}, () => {
      $obj.parent().html(cart_in(id));
    });
  });
});
