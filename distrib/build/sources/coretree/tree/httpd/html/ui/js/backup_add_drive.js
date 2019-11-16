// Function handleNewDrive periodically fetches the status flag and displays
//   it with progress bars as appropriate.

function handleAddFlag(addFlagText) {
  var delay = 1000;

  // Global IDs
  addDriveElem = document.getElementById('buAddDrive');
  okElem = document.getElementById('buOK');
  cancelElem = document.getElementById('buCancel');
  promptElem = document.getElementById('buPrompt');
  inputElem = document.getElementById('buInput');
  nameEntry = document.getElementById('buNameEntry');
  debugElem = document.getElementById('debug');

//debugElem.innerHTML += addFlagText +"\n";

  // Decide what to do
  if (addFlagText == '') {
    // Transiently empty
    delay = .1;

  } else if ((addFlagText.indexOf('Plug in new drive') == 0) ||
             (addFlagText.indexOf('Medium already configured') == 0) ||
             (addFlagText.indexOf('Error:') == 0)) {
    // Display the prompt with the Cancel button
//debugElem.innerHTML += "Plug/Medium/Error:\n";
    promptElem.innerHTML = addFlagText;
    addDriveElem.disabled = true;
    okElem.disabled = true;
    cancelElem.disabled = false;
    inputElem.style.display = 'none';
    // Re-check delay
    delay = .1;

  } else if (addFlagText.indexOf('Enter your name') == 0) {
    // Display the prompt with the OK and Cancel buttons
//debugElem.innerHTML += "Enter(OK)\n";
    promptElem.innerHTML = addFlagText;
    addDriveElem.disabled = true;
    okElem.disabled = false;
    cancelElem.disabled = false;
    inputElem.style.display = 'block';
    // Re-check delay
    delay = .1;

  } else if (addFlagText.indexOf('Remove the backup medium') == 0) {
    // Display the prompt with no buttons
//debugElem.innerHTML += "Remove\n";
    promptElem.innerHTML = addFlagText;
    addDriveElem.disabled = true;
    okElem.disabled = true;
    cancelElem.disabled = true;
    inputElem.style.display = 'none';
    // Re-check delay
    delay = .1;

  } else if (addFlagText.indexOf('Operation') == 0) {
//debugElem.innerHTML += "Operation\n";
    this.location.reload();
    // None shall pass.
  }

  // Re-schedule
  setTimeout ("simpleMonitor(addDriveMonitorObj, '/cgi-bin/txt-bu-addflag.cgi', handleAddFlag)", delay);
}
