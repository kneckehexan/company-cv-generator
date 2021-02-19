$(document).ready(function() {
  console.log('Document ready');
  var educount = 0;
  $('#addedu').on('click',{par1:'edu', par2:educount}, insertTextarea);
});

function insertTextarea(e) {
  $('#' + e.data.par1).append('<label for="' + e.data.par1 + e.data.par2 + '">Utbildning ' + e.data.par2 + ': </label>');
  $('#' + e.data.par1).append('<textarea id="' + e.data.par1 + e.data.par2 + '" name="'+ e.data.par1 + e.data.par2 + '" rows="2" cols="20">');
  e.data.par2++;
  console.log([e.data.par1, e.data.par2]);
}

