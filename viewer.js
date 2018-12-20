const {Format} = require('./settings.js');

var previousItem = null;

function Table() {
  this.table = document.createElement('table');
  this.thead = document.createElement('thead');
  this.tbody = document.createElement('tbody');
  this.table.appendChild(this.thead);
  this.table.appendChild(this.tbody);
}

Table.prototype.getElement = function() {
  return this.table;
}

Table.prototype.setHeader = function(values) {
  var tr = document.createElement('tr');
  Format.forEach(function(item) {
    var size = item.size === undefined ? 1 : item.size;
    for (var i = 0; i < size; ++i) {
      var th = document.createElement('th');
      th.innerText = item.name;
      if (size > 1) {
        th.innerText += '#' + i;
      }
      tr.appendChild(th);
    }
  });
  this.thead.innerHTML = '';
  this.thead.appendChild(tr);
}

Table.prototype.resizeHeader = function() {
  var td = this.tbody.firstChild.children;
  var th = this.thead.firstChild.children;
  for (var i = 0; i < th.length; ++i) {
    th[i].style.width = (td[i].offsetWidth - 2) + 'px';
  }
}

Table.prototype.appendRow = function(values) {
  var tr = document.createElement('tr');
  var j = 0;
  Format.forEach(function(item) {
    var size = item.size === undefined ? 1 : item.size;
    for (var i = 0; i < size; ++i) {
      var td = document.createElement('td');
      td.innerText = values[j];
      td.setAttribute('data-name', item.name);
      td.setAttribute('data-index', 0);
      if (item.size !== undefined) {
       td.setAttribute('data-index', i);
      }
      tr.appendChild(td);
    }
    ++j;
  });
  this.tbody.appendChild(tr);
}

var loadTable = function(data) {
  var lines = data.split("\n");

  var table = new Table();
  table.setHeader(Format);

  for (var i = 0; i < lines.length; ++i) {
    table.appendRow(lines[i].split(" "));
  }

  var node = document.getElementById('output');
  node.innerHTML = '';
  node.appendChild(table.getElement());

  // Update width of table header (required when position: sticky)
  table.resizeHeader()

  function update(target) {
    var node = document.getElementById('panel');
    var name = target.getAttribute('data-name');
    var index = target.getAttribute('data-index');
    var value = parseInt(target.innerText, 16);
    if (name == 'bx') {
      value = parseInt(target.innerText, 10); // decimal!
      node.innerHTML = "<p>bunch crossing " + value + "</p>";
      return;
    }
    if (name == 'muon') {
      var param;
      node.innerHTML = "<p>" + name + "</p>";
      node.innerHTML += "<p>" + value + "</p>";
      param = (value >> 7) & 0xf;
      node.innerHTML += "<p>A: 0x" + param.toString(16) + "</p>";
      param = (value >> 12) & 0xff;
      node.innerHTML += "<p>B: 0x" + param.toString(16) + "</p>";
      param = (value >> 16) & 0xf;
      node.innerHTML += "<p>C: 0x" + param.toString(16) + "</p>";
      return;
    }
    node.innerHTML = "<p>" + value + "</p>";
    return;
  }

  document.addEventListener('click', function(e) {
    if (e.target.tagName == 'TD') {
      update(e.target);
      if (previousItem != null) {
        previousItem.removeAttribute('class');
      }
      e.target.setAttribute('class', 'active');
      previousItem = e.target;
    }
  }, false);
};

module.exports = {
  loadTable
};
