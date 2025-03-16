$(document).ready(function () {
    $('#nav a').on('click', function (ev) {
        const $nav = $("#nav");
        const $current = $(this);
        $nav.scrollLeft(0)
        $scroolleft =
            $current[0].getBoundingClientRect().left - $nav[0].getBoundingClientRect().left
            + ($current[0].getBoundingClientRect().width - $nav[0].getBoundingClientRect().width) / 2
        $nav.scrollLeft($scroolleft)
    })
}
);