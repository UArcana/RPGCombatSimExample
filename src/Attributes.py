attribute_keys = ["str", "agi", "int", "spi", "end", "wis"]


class Attributes:

  def __init__(self):
    self.str = 0
    self.agi = 0
    self.int = 0
    self.spi = 0
    self.end = 0
    self.wis = 0

  def __getitem__(self, key):
    return getattr(self, key)

  def __setitem__(self, key, value):
    if key in attribute_keys:
      setattr(self, key, value)
    else:
      print("Invalid attribute key")
