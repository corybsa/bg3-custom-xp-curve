import os
from pathlib import Path


class XpCurveGenerator:
  def __init__(self):
    self.base_xp_curve = {
      0: 0,
      1: 300,
      2: 600,
      3: 1_800,
      4: 3_800,
      5: 6_500,
      6: 8_000,
      7: 9_000,
      8: 12_000,
      9: 14_000,
      10: 20_000,
      11: 24_000,
      12: 30_000,
    }

    self.custom_xp_curve = self.base_xp_curve.copy()
    self.xp_modifier = 1.0
    self.game_folder = None
    self.curve_file_first_half = os.path.join('Data', 'Public', 'Shared', 'Stats', 'Generated', 'Data', 'XPData.txt')
    self.curve_file_second_half = os.path.join('Data', 'Public', 'SharedDev', 'Stats', 'Generated', 'Data', 'XPData.txt')

    self.modifier_changed_listeners = []

    if os.path.exists('C:\Program Files (x86)\Steam\steamapps\common\Baldurs Gate 3'):
      self.set_game_folder('C:\Program Files (x86)\Steam\steamapps\common\Baldurs Gate 3')
  

  def add_modifier_changed_listener(self, listener: callable):
    self.modifier_changed_listeners.append(listener)
  

  def set_game_folder(self, game_folder: str) -> bool:
    # check if the game folder contains the file 'bg3.exe' in the 'bin' folder
    if self.is_valid_game_folder(game_folder):
      self.game_folder = game_folder
      return True
    
    return False


  def is_valid_game_folder(self, game_folder) -> bool:
    return os.path.exists(os.path.join(game_folder, 'bin', 'bg3.exe'))


  def set_modifier(self, value: float):
    self.xp_modifier = 1 / value

    for level in self.custom_xp_curve:
      self.custom_xp_curve[level] = round(self.base_xp_curve[level] * self.xp_modifier)

    for listener in self.modifier_changed_listeners:
      listener()
  

  def set_level_requirement(self, level: int, value: int):
    self.custom_xp_curve[level] = value
  

  def export_curve(self):
    file1_path = os.path.join(self.game_folder, self.curve_file_first_half)
    file2_path = os.path.join(self.game_folder, self.curve_file_second_half)
    
    # create directories
    Path(os.path.dirname(file1_path)).mkdir(parents=True, exist_ok=True)
    Path(os.path.dirname(file2_path)).mkdir(parents=True, exist_ok=True)

    with open(file1_path, 'w') as file:
      for level in range(1, 6):
        file.write(f'key "Level{level}","{self.custom_xp_curve[level]}"\n\n')
      
      file.write(f'key "MaxXPLevel","5"\n')
    
    with open(file2_path, 'w') as file:
      for level in range(6, len(self.custom_xp_curve)):
        file.write(f'key "Level{level}","{self.custom_xp_curve[level]}"\n\n')
      
      file.write(f'key "MaxXPLevel","{len(self.custom_xp_curve) - 1}"\n')
    
