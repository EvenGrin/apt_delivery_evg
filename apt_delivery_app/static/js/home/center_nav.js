$(document).ready(function () {
  const $nav = $("#nav");
  let $active = $("#nav a.active");
  function scrolling($current) {
    const currentPosition = $nav.scrollLeft(); // Получаем текущее значение прокрутки
    const containerOffsetLeft = $nav[0].getBoundingClientRect().left;
    const elementOffsetLeft = $current[0].getBoundingClientRect().left;
    const elementWidth = $current[0].getBoundingClientRect().width;
    const containerWidth = $nav[0].getBoundingClientRect().width;
    const relativeElementOffsetLeft = elementOffsetLeft - containerOffsetLeft;
    const scrollLeft =
      relativeElementOffsetLeft +
      currentPosition +
      (elementWidth - containerWidth) / 2;
    // Использование animate для плавной прокрутки от текущего положения
    $nav.stop(true, true).animate(
      {
        scrollLeft: scrollLeft,
      },
      500
    );
  }
  $("#nav a").on("click", function (ev) {
    ev.preventDefault(); // Предотвращаем стандартное поведение ссылки
    const $current = $(this);
    scrolling($current);
  });
  $active = $("#nav a.active");
  $(document).on("scroll", function (ev) {
    $current = $("#nav a.active");
    if ($current.html() != $active.html() && $current.length != 0) {
      $active = $current;
      scrolling($current);
    }
  });
});
