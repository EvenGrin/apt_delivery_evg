const form = document.querySelector('form');
if (form) {
  const p = form.querySelectorAll('p')
  p.forEach(p=>{
    p.outerHTML = "<div class='row mb-2 w-100'>"+p.innerHTML+"</div>"
  })
  const inputs = form.querySelectorAll('input[type=email], input[type=password],input[type=date], input[type=time], input[type=datetime-local], input[type=text], textarea');
  inputs.forEach(input => {
    input.classList.add('form-control');
    input.outerHTML = "<div >" + input.outerHTML + "</div>";
  });
  const checkbox = form.querySelectorAll('input[type=checkbox]');
  checkbox.forEach(input => {

    input.outerHTML = "<div class='col-6 d-flex align-items-center'>" + input.outerHTML + "</div>";
  });
  const labels = form.querySelectorAll('label');
  labels.forEach(label => {
    label.classList.add( 'col-form-label');
  });

  const brs = form.querySelectorAll('br');
  brs.forEach(br => {
    br.remove()
  });

  const spans = form.querySelectorAll('span');
  spans.forEach(span => {
    span.classList.add('my-3');
  });

  const button = form.querySelector('button');
  button.classList.add('btn', 'btn-primary', 'btn-block');

  const errorlist = form.querySelectorAll('.errorlist');
  errorlist.forEach(error => {
    error.classList.add('text-danger', 'm-0', 'mt-3');
  });
  form.querySelector('.helptext').classList.add('small')
}

