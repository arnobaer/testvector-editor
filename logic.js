
var prev = null;

var index = [
  {
    name: "Muon",
    index: 0,
    label: "Muon#0"
  },
  {
    name: "Muon",
    index: 1,
    label: "Muon#1"
  },
  {
    name: "Muon",
    index: 2,
    label: "Muon#2"
  }
];

var openFile = function(data) {

  function create_row(tag, values) {
    tr = document.createElement("tr");
    for (var i = 0; i < values.length; ++i) {
       elem = document.createElement(tag);
       if (i < index.length) {
         elem.setAttribute('data-name', index[i].name);
         elem.setAttribute('data-index', index[i].index);
       }
       elem.innerText = values[i];
       tr.appendChild(elem);
    }
    return tr;
  }
  function create_header() {
    var tr = document.createElement("tr");
    for (var i = 0; i < index.length; ++i) {
       elem = document.createElement("th");
       if (i < index.length) {
         elem.innerText = index[i].label;
       }
       else {
         elem.innerText = 'n/a'
       }
       tr.appendChild(elem);
    }
    var thead = document.createElement('thead');
    thead.appendChild(tr);
    return thead;
  }
  function create_data(values) {
    return create_row("td", values);
  }
  var node = document.getElementById('output');

  var table = document.createElement("table");
  var thead = create_header();
  var lines = data.split("\n");
  node.innerHTML = '';

  table.appendChild(thead);
  var tbody = document.createElement('tbody');
  for (var i = 0; i < lines.length; ++i) {
    var row = create_data(lines[i].split(" "));
    tbody.appendChild(row);
  }
  table.appendChild(tbody);
  node.appendChild(table);

  // Update width of table header (required when position: sticky)
  (function() {
    // var td = tbody.firstChild.children;
    // var th = thead.firstChild.children;
    // for (var i = 0; i < th.length; ++i) {
    //   th[i].style.width = (td[i].offsetWidth - 2) + "px";
    // }
  })();

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
    //node.innerHTML = "<p>" + name + "</p>";
    node.innerHTML = "<p>" + value + "</p>";
    return;
  }

  document.addEventListener('click', function(e) {
    if (e.target.tagName == 'TD') {
      update(e.target);
      if (prev != null) {
        prev.removeAttribute('class');
      }
      e.target.setAttribute('class', 'active');
      prev = e.target;
    }
  }, false);
};
