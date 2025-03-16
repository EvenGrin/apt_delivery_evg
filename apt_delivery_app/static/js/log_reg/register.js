const form = document.querySelector('form');
if (form) {
  form.querySelectorAll('p').forEach(p=>{
    p.outerHTML = "<div class='row mb-2 w-100'>"+p.innerHTML+"</div>"
  })

  form.querySelectorAll('input[type=email], input[type=password], input[type=text], input[type=number], textarea').forEach(input => {
    input.classList.add('form-control');
    input.outerHTML = "<div class='col'>" + input.outerHTML + "</div>";
  });
  form.querySelectorAll('select').forEach(input => {
    input.classList.add('form-select');
    input.outerHTML = "<div class='col'>" + input.outerHTML + "</div>";
  });
  form.querySelectorAll('input[type=checkbox]').forEach(input => {
    input.outerHTML = "<div class='col-2 d-flex align-items-center'>" + input.outerHTML + "</div>";
  });

  form.querySelectorAll('label').forEach(label => {
    label.classList.add('col', 'col-form-label');
  });

  form.querySelectorAll('br').forEach(br => {
    br.remove()
  });

  form.querySelectorAll('span').forEach(span => {
    span.classList.add('my-3');
  });

  form.querySelector('button').classList.add('btn', 'btn-primary', 'btn-block');

  form.querySelectorAll('.errorlist').forEach(error => {
    error.classList.add('text-danger');
  });
}