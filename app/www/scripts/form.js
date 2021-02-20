$(document).ready(function() {
  console.log('Document ready');

  // Counters to keep track of the number of textareas in the various categories.
  var counters = {
    edu:0,
    emp:0,
    cou:0,
    ass:0
  };

  // To store all responses.

  // Add textarea
  $('#addedu').on('click', {par1:'edu', par2:counters.edu}, insertTextarea);
  $('#addemp').on('click', {par1:'emp', par2:counters.emp}, insertTextarea);
  $('#addcou').on('click', {par1:'cou', par2:counters.cou}, insertTextarea);
  $('#addass').on('click', {par1:'ass', par2:counters.ass}, insertTextarea);
  
  $('#form').on('submit', function(e) {
    e.preventDefault();
    let form = $('#form')[0];
    let formData = new FormData(form);
    console.log('\nData to be sent: ');
    for (var pair of formData.entries()) {
      console.log('Label: ' + pair[0] + 'Values: ' + pair[1]);
    }
  });
});

/*
 * Function to add a textarea for a particular category. Also adds delete button.
 */
function insertTextarea(e) {
  e.preventDefault();
  // div
  $('#' + e.data.par1).append('<div id="div' + e.data.par1 + e.data.par2 + '">');
  $('#' + e.data.par1).append('</div>');

  // title
  $('#div' + e.data.par1 + e.data.par2).append('<label for="' + e.data.par1 + e.data.par2 + '-title">Titel: </label>');
  $('#div' + e.data.par1 + e.data.par2).append('<input type="text" id="' + e.data.par1 + e.data.par2 + '-title" name="'+ e.data.par1 + '-title">');

  // description
  if (e.data.par1 == 'ass'){
    $('#div' + e.data.par1 + e.data.par2).append('<label for="' + e.data.par1 + e.data.par2 + '-descr">Beskrivning: </label>');
    $('#div' + e.data.par1 + e.data.par2).append('<textarea id="' + e.data.par1 + e.data.par2 + '-descr" name="'+ e.data.par1 + '-descr" rows="5" cols="40">');
  }

  // time
  $('#div' + e.data.par1 + e.data.par2).append('<label for="' + e.data.par1 + e.data.par2 + '-time">Tid: </label>');
  $('#div' + e.data.par1 + e.data.par2).append('<input type="text" id="' + e.data.par1 + e.data.par2 + '-time" name="'+ e.data.par1 + '-time" rows="1" cols="10" pattern="\d{4}" placeholder="yyyy">');

  $('#div' + e.data.par1 + e.data.par2).append('<button onclick="deleteTextarea(\'div' + e.data.par1 + e.data.par2 + '\');" id="del' + e.data.par1 + e.data.par2 + '">Ta bort</button>');
  e.data.par2++;
}

/*
 * Function to remove the textarea incase it is unsued.
 */
function deleteTextarea(areadiv) {
  $('#' + areadiv).remove();
}
