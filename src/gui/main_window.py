import dearpygui.dearpygui as dpg
import os

from xp_curve_generator import XpCurveGenerator
from .xp_curve_window import XpCurveWindow
from .base_window import BaseWindow
from .save_curve_window import SaveCurveWindow


class MainWindow(BaseWindow):
  def __init__(self):
    self.generator = XpCurveGenerator()
    self.main_window_tag = self.get_random_tag()
    self.xp_curve_window = None
    self.save_curve_window = None

    dpg.create_context()

    if(os.path.isfile('config.ini') and os.path.exists('config.ini')):
      dpg.configure_app(init_file='config.ini')
    
    dpg.create_viewport(title='BG3 XP Curve Editor', width=700, height=600)
    dpg.setup_dearpygui()
    dpg.show_viewport()

    self.create_windows()

    dpg.start_dearpygui()
    dpg.destroy_context()


  def create_windows(self):
    with dpg.window(label='Main', tag=self.main_window_tag, show=True, no_close=True):
      dpg.set_primary_window(self.main_window_tag, True)
    
    self.xp_curve_window = XpCurveWindow(self.generator)
    self.save_curve_window = SaveCurveWindow(self.generator)
