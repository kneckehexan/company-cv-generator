$(document).ready(function() {
  console.log('Document ready');

  // localStorage to save user entries.
  const MYSTORE = window.localStorage;

  getEntries(MYSTORE);

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
    storeEntries(MYSTORE, formData);
    this.submit();
  });
});

/*
 * Function to add a textarea for a particular category. Also adds delete button.
 */
function insertTextarea(e, title='', time='', descr='') {
  e.preventDefault();
  // div
  $('#' + e.data.par1).append('<div id="div' + e.data.par1 + e.data.par2 + '">');
  $('#' + e.data.par1).append('</div>');

  // title
  $('#div' + e.data.par1 + e.data.par2).append('<label for="' + e.data.par1 + e.data.par2 + '-title">Titel: </label>');
  $('#div' + e.data.par1 + e.data.par2).append('<input type="text" id="' + e.data.par1 + e.data.par2 + '-title" name="'+ e.data.par1 + '-title" required>');
  $('#' + e.data.par1 + e.data.par2 + '-title').val(title);

  // description
  if (e.data.par1 == 'ass'){
    $('#div' + e.data.par1 + e.data.par2).append('<label for="' + e.data.par1 + e.data.par2 + '-descr">Beskrivning: </label>');
    $('#div' + e.data.par1 + e.data.par2).append('<textarea id="' + e.data.par1 + e.data.par2 + '-descr" name="'+ e.data.par1 + '-descr" rows="5" cols="40">');
    $('#' + e.data.par1 + e.data.par2 + '-descr').val(descr);
  }

  // time
  $('#div' + e.data.par1 + e.data.par2).append('<label for="' + e.data.par1 + e.data.par2 + '-time">År: </label>');
  $('#div' + e.data.par1 + e.data.par2).append('<input type="text" id="' + e.data.par1 + e.data.par2 + '-time" name="'+ e.data.par1 + '-time" rows="1" cols="10" pattern="^\\d{4}$" placeholder="yyyy">');
  $('#' + e.data.par1 + e.data.par2 + '-time').val(time);

  $('#div' + e.data.par1 + e.data.par2).append('<button onclick="deleteTextarea(\'div' + e.data.par1 + e.data.par2 + '\');" id="del' + e.data.par1 + e.data.par2 + '">Ta bort</button>');
  e.data.par2++;
}

/*
 * Function to remove the textarea incase it is unused.
 */
function deleteTextarea(areadiv) {
  $('#' + areadiv).remove();
}

/*
 * Function to save entries in localStorage and show user
 * what is being sent, in console
 */
function storeEntries(ls, fd) {
  var object = {}
  fd.forEach((value, key) => {
    if (!Reflect.has(object, key)) {
      object[key] = value;
      return;
    }
    if (!Array.isArray(object[key])) {
      object[key] = [object[key]];
    }
    object[key].push(value);
  });
  $.each(object, (key,val) => {
    ls.setItem(key, JSON.stringify(val))
  });
  console.log(JSON.stringify(object));
}

/*
 * Function to read any stored items and populate form
 */
function getEntries(ls){
  // Make sure ls isn't empty
  if (window.localStorage.length == 0) {
    return;
  }

  // Single values populate form directly.
  // Multiple values are extracted into a more complex structure
  var tmp_obj = {};
  var arr = [];
  Object.keys(ls).forEach(function(k) {
    if (/^(?!\w{3}-).*/.test(k)) {
      $('#' + k).val(JSON.parse(ls.getItem(k)));
    } else {
      arr.push(JSON.parse(ls.getItem(k)))
      t = k.split(/-\w+$/)[0];
      tmp_obj[t] = {...arr};
    }
  });
  console.log(tmp_obj);


}



//      var arr = JSON.parse(ls.getItem(k));
//      let tmp_sub_obj = {}
////      tmp_sub_obj[k.split(/-\w+$/)] = [arr]
//      tmp_sub_obj[k] = [arr]
//      tmp_arr.push(tmp_sub_obj);
//  var tmp_obj = {
//    'edu-title': [],
//    'edu-time': [],
//    'emp-title': [],
//    'emp-time': [],
//    'cou-title': [],
//    'cou-time': [],
//    'ass-title': [],
//    'ass-time': [],
//    'ass-decr': []
//  };

  // Transform data into a more comprehensible Object.

//  var tmp_obj = {};
//  for (let i = 0; i < tmp_arr.length; i++) {
//    Object.keys(tmp_arr[i]).forEach(function(k) {
//      tmp_obj[k] = tmp_arr[i][k];
//    });
//  }

//  for (let key, val in tmp_obj) {
//    
//  }

//  pasteStorageValues(tmp_obj);

function zip(arrays) {
  return arrays[0].map(function(_,i){
    return arrays.map(function(array){return array[i]})
  });
}
//function pasteStorageValues(obj, section){
//  $.each(obj, function(index, value, section) {
//    insertTextarea({par1:section, par2:counters.section}, value
//}
