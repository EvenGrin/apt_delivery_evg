const form = document.querySelector('form');
if (form) {
  const p = form.querySelectorAll('p')
  p.forEach(p=>{
    p.outerHTML = "<div class='row mb-2 w-100'>"+p.innerHTML+"</div>"
  })
  const inputs = form.querySelectorAll('input, textarea');
  inputs.forEach(input => {
    input.classList.add('form-control', "col-6");
    input.outerHTML = "<div class='col-6'>" + input.outerHTML + "</div>";
  });
  const labels = form.querySelectorAll('label');
  labels.forEach(label => {
    label.classList.add('col-6', 'col-form-label');
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
}