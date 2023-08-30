import dearpygui.dearpygui as dpg
import os
from .base_window import BaseWindow


class MainWindow(BaseWindow):
  def __init__(self):
    dpg.create_context()

    if(os.path.isfile('bark.ini') and os.path.exists('bark.ini')):
      dpg.configure_app(init_file='bark.ini')
    
    dpg.create_viewport(
      title='Wakeful Games Text to Speech Generator',
      width=865,
      height=600
    )
    dpg.setup_dearpygui()
    dpg.show_viewport()

    self.create_windows()

    dpg.start_dearpygui()
    dpg.destroy_context()
