import dearpygui.dearpygui as dpg
from xp_curve_generator import XpCurveGenerator
from .base_window import BaseWindow


class XpCurveWindow(BaseWindow):
  def __init__(self, generator: XpCurveGenerator):
    self.generator = generator
    self.tag = self.get_random_tag()
    self.table_cell_tag = self.get_random_tag()
    self.modifier_slider_tag = self.get_random_tag()
    self.generator.add_modifier_changed_listener(self.update_table)

    with dpg.window(label='XP Curve', tag=self.tag, show=True, pos=[20, 20], width=600, height=190, no_close=True):
      dpg.add_text('This table will update as you change the modifier.\nThe values shown will be the new requirements for each level.')
      self.create_table()
      self.create_slider()


  def create_table(self):
    with dpg.table(header_row=False):
      dpg.add_table_column()
      dpg.add_table_column()
      dpg.add_table_column()

      for row in range(4):
        with dpg.table_row():
          for col in range(3):
            cell = (row + (4 * col)) + 1
            dpg.add_input_int(
              label=f'Level {cell}',
              tag=f'{self.table_cell_tag}_{cell}',
              default_value=self.generator.custom_xp_curve[cell],
              min_value=1,
              min_clamped=True,
              max_value=999999999,
              max_clamped=True,
              callback=lambda id, value: self.check_value(int(id.split('_')[-1]), value),
              on_enter=True
            )

            # show default values in tooltips
            with dpg.tooltip(f'{self.table_cell_tag}_{cell}'):
              dpg.add_text(f'Default value: {self.generator.base_xp_curve[cell]}')
  

  def create_slider(self):
    dpg.add_slider_float(
      label='XP Modifier (?)',
      tag=self.modifier_slider_tag,
      default_value=1.0,
      min_value=0.1,
      max_value=20.0,
      clamped=True,
      width=200,
      format='%.2f',
      callback=lambda id, value: self.generator.set_modifier(value)
    )

    with dpg.tooltip(self.modifier_slider_tag):
      dpg.add_text('''Drag slider to change the XP modifier.
Ctrl + click to enter a specific value.
The XP modifier is a multiplier that is applied to the XP curve.
The higher the modifier, the faster you will level up.
The lower the modifier, the slower you will level up.
If you want to level up twice as fast, set the modifier to 2.
If you want to level up 15% faster, set the modifier to 1.15.
If you want to level up slower, set the modifier to a value less than 1.
THIS WILL OVERRIDE ANY MANUAL CHANGES YOU MAKE TO THE XP CURVE!''')
  

  def update_table(self):
    for row in range(4):
      for col in range(3):
        cell = (row + (4 * col)) + 1
        dpg.configure_item(f'{self.table_cell_tag}_{cell}', default_value=self.generator.custom_xp_curve[cell])
  

  def check_value(self, current_level: int, value: int):
    self.generator.set_level_requirement(current_level, value)
    max_level = len(self.generator.custom_xp_curve)
    
    # check if the value is greater than the next level's requirement
    if current_level < max_level:
      # loop through the remaining levels
      for next_level in range(current_level + 1, max_level):
        # get the next value in the curve
        next_value = self.generator.custom_xp_curve[next_level]
        diff = next_level - current_level

        if value >= next_value - diff:
          self.generator.set_level_requirement(next_level, value + diff)
          dpg.configure_item(f'{self.table_cell_tag}_{next_level}', default_value=value + diff)
    
    # check if the value is less than the previous level's requirement
    if current_level > 1:
      # loop through the previous levels
      for prev_level in range(current_level - 1, 0, -1):
        # get the previous value in the curve
        prev_value = self.generator.custom_xp_curve[prev_level]
        diff = current_level - prev_level

        if value <= prev_value + diff:
          self.generator.set_level_requirement(prev_level, value - diff)
          dpg.configure_item(f'{self.table_cell_tag}_{prev_level}', default_value=value - diff)

