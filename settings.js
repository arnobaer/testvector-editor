
var BunchCrossing = {
  name: "bx",
  size: 1,
  base: 10,
  attributes: []
};

var Muon = {
  name: "muon",
  size: 8,
  base: 16,
  attributes: [
    {name: "phi", slice: [9, 0]},
    {name: "pt", slice: [18, 10]},
    {name: "quality", slice: [22, 19]},
    {name: "eta", slice: [31, 23]},
    {name: "iso", slice: [33, 32]},
    {name: "charge_sign", slice: [34]},
    {name: "charge_valid", slice: [35]},
    {name: "reserved", slice: [63, 36]}
  ]
};

var Egamma = {
  name: "eg",
  size: 12,
  base: 16,
  attributes: [
    {name: "et", slice: [8, 0]},
    {name: "eta", slice: [16, 9]},
    {name: "phi", slice: [24, 17]},
    {name: "iso", slice: [26, 25]},
    {name: "reserved", slice: [31, 27]}
  ]
};

var Tau = {
  name: "tau",
  size: 12,
  base: 16,
  attributes: [
    {name: "et", slice: [8, 0]},
    {name: "eta", slice: [16, 9]},
    {name: "phi", slice: [24, 17]},
    {name: "iso", slice: [26, 25]},
    {name: "reserved", slice: [31, 27]}
  ]
};

var Jet = {
  name: "jet",
  size: 12,
  base: 16,
  attributes: [
    {name: "et", slice: [10, 0]},
    {name: "eta", slice: [18, 11]},
    {name: "phi", slice: [26, 19]},
    {name: "reserved", slice: [31, 27]}
  ]
};

var Et = {
  name: "et",
  size: 1,
  base: 16,
  attributes: [
    {name: "et", slice: [11, 0]},
    {name: "reserved", slice: [27, 12]},
    {name: "MBT0HFP", slice: [31, 28]}
  ]
};

var Ht = {
  name: "ht",
  size: 1,
  base: 16,
  attributes: [
    {name: "et", slice: [11, 0]},
    {name: "reserved", slice: [27, 12]},
    {name: "MBT0HFM", slice: [31, 28]}
  ]
};

var Etm = {
  name: "etm",
  size: 1,
  base: 16,
  attributes: [
    {name: "et", slice: [11, 0]},
    {name: "phi", slice: [19, 12]},
    {name: "reserved", slice: [27, 18]},
    {name: "MBT1HFP", slice: [31, 28]}
  ]
};

var Htm = {
  name: "htm",
  size: 1,
  base: 16,
  attributes: [
    {name: "et", slice: [11, 0]},
    {name: "phi", slice: [19, 12]},
    {name: "reserved", slice: [27, 18]},
    {name: "MBT1HFM", slice: [31, 28]}
  ]
};

var Empty = {
  name: "empty",
  size: 8,
  base: 16,
  attributes: []
};

var External = {
  name: "external",
  size: 1,
  base: 16,
  attributes: []
};

var Algorithms = {
  name: "algorithms",
  size: 1,
  base: 16,
  attributes: []
};

var Finor = {
  name: "finor",
  size: 1,
  base: 16,
  attributes: []
};

var Format = (function() {
  var items = [BunchCrossing, Muon, Egamma, Tau, Jet, Et, Ht, Etm, Htm, Empty, External, Algorithms, Finor];
  return items;
})();

module.exports = {
  Format
};
