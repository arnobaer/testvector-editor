const {app, dialog, BrowserWindow, Menu} = require('electron');
const url = require('url');
const path = require('path');
const fs = require('fs');

function accel(accelerator) {
  if (process.platform == 'darwin')
    return accelerator.replace('Ctrl', 'Command');
  return accelerator.replace('Command', 'Ctrl');
}

let window;

const menuTemplate = [
  {
    label: 'File',
    submenu: [
      {
        label: 'Open File...',
        accelerator: accel('Ctrl+O'),
        click() {
          dialog.showOpenDialog(function(fileNames) {
            // fileNames is an array that contains all the selected
            if(fileNames === undefined){
              console.log("No file selected");
              return;
            }

            fs.readFile(fileNames[0], 'utf-8', function(err, data) {
              if(err) {
                alert("An error ocurred reading the file :" + err.message);
                return;
              }

              window.webContents.send('item:load', data);
            });
          });
        }
      },
      {
        label: 'Save As...',
        accelerator: accel('Ctrl+Shift+S'),
        click() {}
      },
      {
        label: 'Quit',
        accelerator: accel('Ctrl+Q'),
        click() {
          app.quit();
        }
      }
    ]
  },
  {
    label: 'DevTools',
    submenu: [
      {
        label: 'Toggle DevTools',
        click(item, focusedWindow) {
          focusedWindow.toggleDevTools();
        }
      }
    ]
  }
];

app.on('ready', function() {
  window = new BrowserWindow();

  window.loadURL(url.format({
    pathname: path.join(__dirname, 'index.html'),
    protocol: 'file',
    slashes: true
  }));

  const menu = Menu.buildFromTemplate(menuTemplate);
  Menu.setApplicationMenu(menu);

});
