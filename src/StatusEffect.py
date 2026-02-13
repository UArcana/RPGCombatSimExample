class StatusEffect:

  def __init__(self, applier, appliedto, type, duration = None, data = {}):
    self.type = type
    self.applier = applier
    self.appliedto = appliedto
    self.duration = duration
    self.data = data

  def on_game_tick(self, duration=0.01):
    if self.duration is not None:
      self.duration -= duration
      if self.duration <= 0:
         self.appliedto.remove_status_effect(self)
