var btn = document.getElementById('btn-rh2');
btn.addEventListener('click', function(){
  var card = document.getElementById('cardRH');
  var input2 = document.createElement('input');
  var d = document.createElement('div');
  d.setAttribute('class', 'form-group');
  input2.setAttribute('type', 'text');
  input2.setAttribute('name', 'name');
  input2.setAttribute('class', 'form-control');
  d.appendChild(input2);
  card.appendChild(d)
})