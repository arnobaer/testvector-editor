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
  var column = 0;
  Format.forEach(function(item) {
    var size = item.size === undefined ? 1 : item.size;
    var td;
    for (var i = 0; i < size; ++i) {
      td = document.createElement('td');
      td.innerText = values[column];
      td.setAttribute('data-name', item.name);
      td.setAttribute('data-index', 0);
      if (item.size !== undefined) {
       td.setAttribute('data-index', i);
      }
      tr.appendChild(td);
      ++column;
    }
  });
  this.tbody.appendChild(tr);
}

var loadTable = function(data) {
  var lines = data.split(/\n\r|\n/gm);

  // Create table
  var table = new Table();
  table.setHeader(Format);

  // Fill table with data
  lines.forEach(function(line) {
    if (line != '') {
      table.appendRow(line.split(/\s+/gm));
    }
  });

  var node = document.getElementById('output');
  node.innerHTML = '';
  node.appendChild(table.getElement());

  // Update width of table header (required when position: sticky)
  table.resizeHeader()

  function bitmask(width) {
    return parseInt('1'.repeat(width), 2) ;
  }

  function update(target) {
    var node = document.getElementById('panel');
    var name = target.getAttribute('data-name');
    var index = target.getAttribute('data-index');
    var item = Format.find(function(item) {
      return item.name == name;
    });
    var value = parseInt(target.innerText, item.base);
    if (index > 1) {
      node.innerHTML = "<p>" + name + "#" + index + "</p>";
    }
    else {
      node.innerHTML = "<p>" + name + "</p>";
    }
    node.innerHTML = "<p>" + name + "</p>";
    node.innerHTML += "<p>" + target.innerText + "</p>";
    item.attributes.forEach(function(attribute) {
      var msb = attribute.slice[0];
      var lsb = attribute.slice[attribute.slice.length - 1];
      if (msb == lsb) msb += 1;
      // TODO: BUG: Does not work for 64bit muons !
      var param = (value >>> lsb) & bitmask(msb - lsb);
      var slice = attribute.slice.join(':');
      node.innerHTML += "<p>" + attribute.name + " [" + slice + "]: 0x" + param.toString(16) + "</p>";
    });
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
