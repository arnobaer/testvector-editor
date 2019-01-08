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
        return ((1 << self.bitwidth) - 1)
    @property
    def charwidth(self):
        return int(math.ceil(self.bitwidth / 4.))
    def get(self, value):
        return (value >> self.lsb) & self.bitmask

class ObjectFormat:
    width = 32
    base = 16
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

class MuonFormat(ObjectFormat):
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

class EgammaFormat(ObjectFormat):
    name = 'eg'
    attributes = [
        Attribute("et", [8, 0]),
        Attribute("eta", [16, 9]),
        Attribute("phi", [24, 17]),
        Attribute("iso", [26, 25]),
        Attribute("reserved", [31, 27]),
    ]

class TauFormat(ObjectFormat):
    name = 'tau'
    attributes = [
        Attribute("et", [8, 0]),
        Attribute("eta", [16, 9]),
        Attribute("phi", [24, 17]),
        Attribute("iso", [26, 25]),
        Attribute("reserved", [31, 27]),
    ]

class JetFormat(ObjectFormat):
    name = 'jet'
    attributes = [
        Attribute("et", [10, 0]),
        Attribute("eta", [18, 11]),
        Attribute("phi", [26, 19]),
        Attribute("reserved", [31, 27]),
    ]

class EtFormat(ObjectFormat):
    name = 'et'
    attributes = [
        Attribute("et", [11, 0]),
        Attribute("reserved", [27, 12]),
        Attribute("MBT0HFP", [31, 28]),
    ]

class HtFormat(ObjectFormat):
    name = 'ht'
    attributes = [
        Attribute("et", [11, 0]),
        Attribute("reserved", [27, 12]),
        Attribute("MBT0HFM", [31, 28]),
    ]

class EtmFormat(ObjectFormat):
    name = "etm"
    attributes = [
        Attribute("et", [11, 0]),
        Attribute("phi", [19, 12]),
        Attribute("reserved", [27, 18]),
        Attribute("MBT1HFP", [31, 28]),
    ]

class HtmFormat(ObjectFormat):
    name = "htm"
    attributes = [
        Attribute("et", [11, 0]),
        Attribute("phi", [19, 12]),
        Attribute("reserved", [27, 18]),
        Attribute("MBT1HFM", [31, 28]),
    ]

class EmptyFormat(ObjectFormat):
    name = "empty"

class ExternalFormat(ObjectFormat):
    name = "external"
    width = 256
    attributes = [Attribute(str(i), [i]) for i in range(width)]

class AlgorithmsFormat(ObjectFormat):
    name = "algorithms"
    width = 512
    attributes = [Attribute(str(i), [i]) for i in range(width)]

class FinorFormat(ObjectFormat):
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
