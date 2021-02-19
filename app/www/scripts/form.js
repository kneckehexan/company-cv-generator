$(document).ready(function() {
  console.log('Document ready');
  var educount = 0;
  $('#addeducation').on('click', insertTextarea('edu',educount));
});

function insertTextarea(area, counter) {
  $('#' + area).append('<label for="' + area + counter + '">Utbildning ' + counter + ': </label>');
  $('#' + area).append('<textarea id="' + area + counter + '" name="'+ area + counter + '" placeholer="Namn på "' + area + '>');
  counter++;
  console.log([area, counter]);
}

