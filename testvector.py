import math

# -----------------------------------------------------------------------------
#  Test Vector
# -----------------------------------------------------------------------------

class Attribute:
    def __init__(self, name, slice):
        self.name = name
        self.msb = slice[0]
        self.lsb = slice[-1]
    @property
    def bitwidth(self):
        return (self.msb - self.lsb) + 1
    @property
    def bitmask(self):
        return ((1 << self.bitwidth) - 1) << self.lsb
    @property
    def charwidth(self):
        return int(math.ceil(self.bitwidth / 4.))
    def get(self, value):
        return (value & self.bitmask) >> self.lsb

class Format:
    width = 32
    name = None
    attributes = []
    def __init__(self, index):
        self.index = index
    def format(self, value):
        return "{0:0{1}x}".format(value, self.charwidth)
    def label(self):
        if self.index is not None:
            return "{}[{}]".format(self.name, self.index)
        return self.name
    @property
    def charwidth(self):
        return int(math.ceil(self.width / 4.))

class MuonFormat(Format):
    width = 64
    name = 'muon'
    attributes = [
        Attribute("phi", [9, 0]),
        Attribute("pt", [18, 10]),
        Attribute("quality", [22, 19]),
        Attribute("eta", [31, 23]),
        Attribute("iso", [33, 32]),
        Attribute("charge_sign", [34]),
        Attribute("charge_valid", [35]),
        Attribute("reserved", [63, 36]),
    ]

class EgammaFormat(Format):
    name = 'eg'
    attributes = [
        Attribute("et", [8, 0]),
        Attribute("eta", [16, 9]),
        Attribute("phi", [24, 17]),
        Attribute("iso", [26, 25]),
        Attribute("reserved", [31, 27]),
    ]

class TauFormat(Format):
    name = 'tau'
    attributes = [
        Attribute("et", [8, 0]),
        Attribute("eta", [16, 9]),
        Attribute("phi", [24, 17]),
        Attribute("iso", [26, 25]),
        Attribute("reserved", [31, 27]),
    ]

class JetFormat(Format):
    name = 'jet'
    attributes = [
        Attribute("et", [10, 0]),
        Attribute("eta", [18, 11]),
        Attribute("phi", [26, 19]),
        Attribute("reserved", [31, 27]),
    ]

class EtFormat(Format):
    name = 'et'
    attributes = [
        Attribute("et", [11, 0]),
        Attribute("reserved", [27, 12]),
        Attribute("MBT0HFP", [31, 28]),
    ]

class HtFormat(Format):
    name = 'ht'
    attributes = [
        Attribute("et", [11, 0]),
        Attribute("reserved", [27, 12]),
        Attribute("MBT0HFM", [31, 28]),
    ]

class EtmFormat(Format):
    name = "etm"
    attributes = [
        Attribute("et", [11, 0]),
        Attribute("phi", [19, 12]),
        Attribute("reserved", [27, 18]),
        Attribute("MBT1HFP", [31, 28]),
    ]

class HtmFormat(Format):
    name = "htm"
    attributes = [
        Attribute("et", [11, 0]),
        Attribute("phi", [19, 12]),
        Attribute("reserved", [27, 18]),
        Attribute("MBT1HFM", [31, 28]),
    ]

class EmptyFormat(Format):
    name = "empty"

def vector_attributes(width):
    """Returns list of attributes for every bith in width."""
    return [Attribute(str(i), [i]) for i in range(width)]

class ExternalFormat(Format):
    name = "external"
    width = 256
    attributes = vector_attributes(width)

class AlgorithmsFormat(Format):
    name = "algorithms"
    width = 512
    attributes = vector_attributes(width)

class FinorFormat(Format):
    name = "finor"
    width = 1

class TestVector:

    def __init__(self):
        self.formats = []
        self.addFormat(MuonFormat, 8)
        self.addFormat(EgammaFormat, 12)
        self.addFormat(TauFormat, 12)
        self.addFormat(JetFormat, 12)
        self.addFormat(EtFormat)
        self.addFormat(HtFormat)
        self.addFormat(EtmFormat)
        self.addFormat(HtmFormat)
        self.addFormat(EmptyFormat, 8)
        self.addFormat(ExternalFormat)
        self.addFormat(AlgorithmsFormat)
        self.addFormat(FinorFormat)
        self.events = []

    def addFormat(self, cls, count=1):
        self.formats += [cls(i) for i in range(count)]

    def read(self, f):
        self.events = []
        for line in f:
            items = line.strip().split()
            bx = int(items.pop(0)) # ignore
            data = []
            for fmt in self.formats:
                data.append(int(items.pop(0), 16))
            self.events.append(data)
