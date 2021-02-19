$(document).ready(function() {
  console.log('Document ready');
  var counters = {
    edu:0,
    emp:0,
    cou:0,
    ass:0
  };
  // Add textarea
  $('#addedu').on('click', {par1:'edu', par2:counters.edu}, insertTextarea);
  $('#addemp').on('click', {par1:'emp', par2:counters.emp}, insertTextarea);
  $('#addcou').on('click', {par1:'cou', par2:counters.cou}, insertTextarea);
  $('#addass').on('click', {par1:'ass', par2:counters.ass}, insertTextarea);
  
  // Remove textarea
  $('button').on('click', function(){
    return this.id
  });
});

function insertTextarea(e) {
  $('#' + e.data.par1).append('<div id="div' + e.data.par1 + e.data.par2 + '">');
  $('#' + e.data.par1).append('</div>');
  $('#div' + e.data.par1 + e.data.par2).append('<label for="' + e.data.par1 + e.data.par2 + '">Lägg till här: </label>');
  $('#div' + e.data.par1 + e.data.par2).append('<textarea id="' + e.data.par1 + e.data.par2 + '" name="'+ e.data.par1 + e.data.par2 + '" rows="2" cols="20">');
  $('#div' + e.data.par1 + e.data.par2).append('<button onclick="deleteTextarea(\'div' + e.data.par1 + e.data.par2 + '\');" id="del' + e.data.par1 + e.data.par2 + '">Ta bort</button>');
  e.data.par2++;
}

function deleteTextarea(areadiv) {
  $('#' + areadiv).remove();
}
