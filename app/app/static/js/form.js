// Counters to keep track of the number of textareas in the various categories.
var counters = {
  edu:0,
  emp:0,
  cou:0,
  ass:0
};


$(document).ready(function() {
  console.log('Document ready');

  // localStorage to save user entries.
  const MYSTORE = window.localStorage;

  getEntries(MYSTORE);


  // Add textarea
  $('#addedu').on('click', function() {
    insertTextarea('edu', counters.edu);
  });
  $('#addemp').on('click', function() {
    insertTextarea('emp', counters.emp);
  });
  $('#addcou').on('click', function() {
    insertTextarea('cou', counters.cou);
  });
  $('#addass').on('click', function() {
    insertTextarea('ass', counters.ass);
  });
  

  // Submit and store form values
  $('#form').on('submit', function(e) {
    e.preventDefault();
    let form = $('#form')[0];
    let formData = new FormData(form);
    console.log('\nData to be sent: ');
    for (let pair of formData.entries()) {
      console.log(pair[0] + ', ' + pair[1]);
    }
    storeEntries(MYSTORE, formData, counters);
    this.submit();
  });

  $('#resetForm').on('click', {c:counters}, resetForm);
  $('#clearLs').on('click', clearLs);
});

/*
 * Function to add a textarea for a particular category. Also adds delete button.
 */
function insertTextarea(cat, catcount) {
//  e.preventDefault();
  // new div
  $('#' + cat).append('<div id="div' + cat + catcount + '">');
  $('#' + cat).append('</div>');

  // title
  inputEntry(cat, catcount, 'title', 'Titel', 'text');

  // If assignment
  if (cat == 'ass'){
    inputEntry(cat, catcount, 'company', 'Företag', 'text'); // Company
    inputEntry(cat, catcount, 'role', 'Roll', 'text'); // Role
    inputEntry(cat, catcount, 'descr', 'Beskrivning', 'textarea'); // Description
  }

  // time
  inputEntry(cat, catcount, 'time', 'Tid', 'time')

  // delete
  $('#div' + cat + catcount).append('<button onclick="deleteTextarea(\'div' + cat + catcount + '\');" id="del' + cat + catcount + '">Ta bort</button>');
  counters[cat]++;
}

/*
 * Function to remove the textarea incase it is unused.
 */
function deleteTextarea(areadiv) {
  let del = confirm('Bekräfta borttagning');
  if (del){
    $('#' + areadiv).remove();
  }
}

/*
 * Function to reset entire form
 */
function resetForm(){
  let del = confirm('Bekräfta nollställning av formulär');
  if (del){
    for (let i = 0; i < counters['edu']; i++) {
      $('#divedu' + i).remove();
    }
    for (let i = 0; i < counters['emp']; i++) {
      $('#divemp' + i).remove();
    }
    for (let i = 0; i < counters['cou']; i++) {
      $('#divcou' + i).remove();
    }
    for (let i = 0; i < counters['ass']; i++) {
      $('#divass' + i).remove();
    }
    $('#form').trigger('reset');
    counters = {
      edu:0,
      emp:0,
      cou:0,
      ass:0
    };
  }
}

/*
 * Helper function to insert new HTML form elements.
 * params:  e1, e2 = event data parameter from jQuery.
 *          htmlPart = String, used for element id and name.
 *          textPart = String, used for visible label text.
 *          type = String, used to check if input element should
 *                  be text or textarea (or 'time', that in this 
 *                  case is the same as 'text' but with a small
 *                  pattern checker enabled.
 */
function inputEntry(e1, e2, htmlPart, textPart, type) {
  $('#div' + e1 + e2).append('<label for="' + e1 + e2 + '-' + htmlPart + '">' + textPart + ': </label>');
  if (type == 'textarea') {
    $('#div' + e1 + e2).append('<textarea id="' + e1 + e2 + '-' + htmlPart + '" name="'+ e1 + '-' + htmlPart + '" rows="5" cols="40">');
    $('#div' + e1 + e2).append('</textarea>');
  } else if (type == 'time') {
    $('#div' + e1 + e2).append('<input type="text" id="' + e1 + e2 + '-' + htmlPart + '" name="'+ e1 + '-' + htmlPart + '" pattern="^\\d{4}" placeholder="Ex. yyyy">');
  } else {
    $('#div' + e1 + e2).append('<input type="' + type + '" id="' + e1 + e2 + '-' + htmlPart + '" name="'+ e1 + '-' + htmlPart + '" required>');
  }
}


/*
 * Function to save entries in localStorage in a particular manner
 * and show user what is being sent, in console
 * params:  ls = Object, localStorage
 *          fd = Object, FormData
 *          counters = Object, counters with info about how many entries
 *            there are per 'education', 'employment' etc.
 */
function storeEntries(ls, fd, counters) {
  var obj = {
    edu: [],
    emp: [],
    cou: [],
    ass: []
  }
  arredu = {};
  arremp = {};
  arrcou = {};
  arrass = {};
  let a1 = 0, b1 = 0, c1 = 0, d1 = 0, a2 = 0, b2 = 0, c2 = 0, d2 = 0;
  for (let pair of fd.entries()){
    if (/^(?!\w{3}-).*/.test(pair[0])) {
      ls.setItem(pair[0], pair[1]);
    } else if(pair[0].includes('edu')) {
      if (pair[0].includes('title')) {
        arrass['title'] = pair[1];
      } else if (pair[0].includes('time')) {
        arrass['time'] = pair[1];
      }
      a1++;
      if (a1 == 2) {
        obj['edu'][a2] = arrass;
        arrass = {};
        a1 = 0;
        a2++;
      }
    } else if (pair[0].includes('emp')) {
      if (pair[0].includes('title')) {
        arremp['title'] = pair[1];
      } else if (pair[0].includes('time')) {
        arremp['time'] = pair[1];
      }
      b1++;
      if (b1 == 2) {
        obj['emp'][b2] = arremp;
        arremp= {};
        b1= 0;
        b2++;
      }
    } else if (pair[0].includes('cou')) {
      if (pair[0].includes('title')) {
        arrcou['title'] = pair[1];
      } else if (pair[0].includes('time')) {
        arrcou['time'] = pair[1];
      }
      c1++;
      if (c1 == 2) {
        obj['cou'][c2] = arrcou;
        arrcou= {};
        c1 = 0;
        c2++;
      }
    } else if (pair[0].includes('ass')) {
      if (pair[0].includes('title')) {
        arrass['title'] = pair[1];
      } else if (pair[0].includes('company')) {
        arrass['company'] = pair[1];
      } else if (pair[0].includes('role')) {
        arrass['role'] = pair[1];
      } else if (pair[0].includes('descr')) {
        arrass['descr'] = pair[1];
      } else if (pair[0].includes('time')) {
        arrass['time'] = pair[1];
      }
      d1++;
      if (d1 == 5) {
        obj['ass'][d2] = arrass;
        arrass= {};
        d1 = 0;
        d2++;
      }
    }
  }
  ls.setItem('mult', JSON.stringify(obj));
  ls.setItem('counters', JSON.stringify(counters));
  console.log(ls);
}

/*
 * Function to read any stored items and populate form
 */
function getEntries(ls){
  // Make sure ls isn't empty
  if (window.localStorage.length == 0) {
    return;
  }

  // Populate form with empty input/textareas, that correspond with
  // the stored values in counters (from localStorage)
  counters = JSON.parse(ls.getItem('counters'));
  for (let [key,val] of Object.entries(counters)) {
    for (let i = 0; i < val; i++) {
      insertTextarea(key, i);
      counters[key]--;
    }
  }

  // Add stored values from localStorage to the newly added
  // input/textarea.
  let tmp_obj = JSON.parse(ls.getItem('mult')); // Parse JSON string in lS
  for (let [key,val] of Object.entries(tmp_obj)) { // iterate over object
    for (let i = 0; i < val.length; i++) { // iterate over array containing values
      for (let [k, v] of Object.entries(val[i])) { // Array contains objects, iterate over these
        $('#' + key + i + '-' + k).val(v); // Insert values in correct input/textarea
      }
    }
  }

  // Add the unique values (such as 'name', 'role' and so on) from 
  // localStorage.
  Object.keys(ls).forEach(function(k) {
    if (/^(?!\w{3}-).*/.test(k)) { // test RegEx with Object key. "if key != 'edu-'" for example.
      $('#' + k).val(ls.getItem(k)); // Populate input/textarea with stored value
    } 
  });
  console.log('Getting from localStorage:');
  console.log(ls);
}


/*
 * Function to clear localStorage completely.
 */
function clearLs() {
  let con = confirm('Är du säker på att du vill radera allt?');
  if (con) localStorage.clear();
}

function zip(arrays) {
  return arrays[0].map(function(_,i){
    return arrays.map(function(array){return array[i]})
  });
}
//function pasteStorageValues(obj, section){
//  $.each(obj, function(index, value, section) {
//    insertTextarea({par1:section, par2:counters.section}, value
//}
