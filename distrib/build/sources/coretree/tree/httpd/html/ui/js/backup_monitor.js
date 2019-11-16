// Function handleFlag periodically fetches the status flag and displays
//   it with progress bars as appropriate.

function handleFlag(flagText) {
  var delay = 1000;
  var Fileno = 0;
  var statElem = document.getElementById('buStatus');
  var progVarElem = document.getElementById('buProgressVar');
  var progTotalElem = document.getElementById('buProgressTotal');

  // Decide what to do
  if (flagText == '') {
    // Transiently empty
    delay = 1;

  } else if ((backupState == 'start') && 
             ((flagText.indexOf('Last backup') == 0  || 
               flagText.indexOf('Last restore') == 0  || 
               flagText.indexOf('Backup scheduled') == 0))) {
    // Wait longer; change isn't imminent
    delay = 1000;
    statElem.innerHTML = flagText;

  } else if ((backupState == 'start') && 
             ((flagText.indexOf('Last backup') == -1 || 
               flagText.indexOf('Last restore') == -1 || 
               flagText.indexOf('Backup scheduled') == -1))) {
    // Look lively, changing to state 'run'
    delay = 1;
    backupState = 'run';
    whichBar = 0;
    progVarElem.style.minWidth = '0';
    progVarElem.style.width = '0';
    progTotalElem.style.minWidth = '0';
    progTotalElem.style.width = '0';
    statElem.innerHTML = flagText;

  } else if ((backupState == 'run') && 
             (flagText.indexOf('var backup complete') == 0)) {
    // Switch to other progress bar
    whichBar = 1;
    progVarElem.style.width = maxwidth.toString() + "em";
    statElem.innerHTML = flagText;

  } else if ((backupState == 'run') && 
             (flagText.indexOf('total backup complete') == 0)) {
    // Slow down a bit, backup is nearly done
    delay = 10;
    progTotalElem.style.width = maxwidth.toString() + "em";
    statElem.innerHTML = flagText;

  } else if ((backupState == 'run') && 
             (flagText.indexOf('Remove') == 0)) {
    // Slow down a lot, we're really done
    delay = 100;
    statElem.innerHTML = removePrompt;

  } else if ((backupState == 'run') && 
             (flagText.indexOf('Last backup') == 0)) {
    // Ease off to a vigorous mosey; we're idle again
    delay = 1000;
    backupState = 'start';
    statElem.innerHTML = flagText;

  } else if ((backupState == 'run') && 
             (flagText.match(/^[0-9]+\/[0-9]+: /) != null)) {
    // display filename & progress bars
    var Fileno = flagText.slice(0, flagText.indexOf('/'));
    var total = flagText.slice(flagText.indexOf('/')+1, flagText.indexOf(':'));
    if (whichBar == 0) {
      progVarElem.style.minWidth = Number(maxwidth*Fileno/total).toString() + 'em';
      progVarElem.style.width = Number(maxwidth*Fileno/total).toString() + 'em';
      progTotalElem.style.minWidth = '0';
      progTotalElem.style.width = '0';
    } else {
      progVarElem.style.minWidth = maxwidth.toString() + 'em';
      progVarElem.style.width = maxwidth.toString() + 'em';
      progTotalElem.style.minWidth = Number(maxwidth*Fileno/total).toString() + 'em';
      progTotalElem.style.width = Number(maxwidth*Fileno/total).toString() + 'em';
    }
    delay = 1;
    statElem.innerHTML = flagText.slice(flagText.indexOf(':')+2);

  } else {
    // Dunno what; ignore quickly
    delay = 1;
    //statElem.innerHTML = flagText;
  }

  // Re-schedule
  setTimeout ("simpleMonitor(backupMonitorObj, '/cgi-bin/txt-bu-flag.cgi', handleFlag)", delay);
}
