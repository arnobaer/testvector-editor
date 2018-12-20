
var BunchCrossing = {
  name: "bx"
};

var Muon = {
  name: "muon",
  size: 8,
  mask: 0xffffffffffffffff,
  attributes: [
    {name: "A", shift: 0, mask: 0xf},
    {name: "B", shift: 7, mask: 0x8f},
    {name: "C", shift: 12, mask: 0xf},
  ]
};

var Format = (function() {
  var items = [BunchCrossing];
  for (var i = 0; i < Muon.size; ++i) {
    items.push(Muon);
  }
  return items;
})();
