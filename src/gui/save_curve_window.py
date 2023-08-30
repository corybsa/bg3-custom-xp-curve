import os
import dearpygui.dearpygui as dpg
from xp_curve_generator import XpCurveGenerator
from .base_window import BaseWindow


class SaveCurveWindow(BaseWindow):
  def __init__(self, generator: XpCurveGenerator):
    self.generator = generator
    self.tag = self.get_random_tag()
    self.game_folder_file_dialog_tag = self.get_random_tag()
    self.game_folder_text_tag = self.get_random_tag()
    self.game_folder_tooltip_tag = self.get_random_tag()

    with dpg.window(label='Save Curve', tag=self.tag, show=True, pos=[20, 230], width=450, height=160, no_close=True):
      self.create_text()
      self.create_file_dialog()
      self.create_buttons()


  def create_file_dialog(self):
    dpg.add_file_dialog(
      tag=self.game_folder_file_dialog_tag,
      directory_selector=True,
      show=False,
      default_filename='',
      width=500,
      height=350,
      file_count=-1,
      default_path=os.path.abspath(os.sep),
      callback=lambda id, value: self.update_game_folder(value['file_path_name'], False)
    )


  def create_buttons(self):
    dpg.add_button(label='Set Game Folder', callback=lambda: dpg.show_item(self.game_folder_file_dialog_tag))
    dpg.add_button(label='Save Curve', callback=lambda: self.save_curve())
  

  def create_text(self):
    dpg.add_text(f'Game Folder: {self.generator.game_folder}', tag=self.game_folder_text_tag)

    with dpg.tooltip(self.game_folder_text_tag, tag=self.game_folder_tooltip_tag):
      dpg.add_text('The game folder is not set. You can set it by clicking the button below.')
    
    self.update_game_folder(self.generator.game_folder, True)
  

  def update_game_folder(self, value, is_init: bool):
    is_valid = False

    if value is not None:
      is_valid = self.generator.set_game_folder(value)
    
    if is_valid:
      dpg.set_value(self.game_folder_text_tag, f'Game Folder:\n{self.generator.game_folder}')
      dpg.hide_item(self.game_folder_tooltip_tag)
      dpg.set_item_width(self.tag, len(self.generator.game_folder) * 7 + 20)
    else:
      dpg.set_value(self.game_folder_text_tag, 'Game Folder: None (?)')
      dpg.show_item(self.game_folder_tooltip_tag)

      if not is_init:
        self.open_modal('Invalid game folder', no_close=False)


  def save_curve(self):
    if self.generator.game_folder is not None and self.generator.is_valid_game_folder(self.generator.game_folder):
      self.generator.export_curve()
      self.open_modal('Curve saved', no_close=False)
    else:
      self.open_modal('Please specify your game install folder', no_close=False)

