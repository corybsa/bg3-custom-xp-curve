import dearpygui.dearpygui as dpg
from xp_curve_generator import XpCurveGenerator
from .base_window import BaseWindow


class XpCurveWindow(BaseWindow):
  def __init__(self, generator: XpCurveGenerator):
    self.generator = generator
    self.tag = self.get_random_tag()
    self.table_tag = self.get_random_tag()
    self.table_cell_tag = self.get_random_tag()
    self.modifier_slider_tag = self.get_random_tag()
    self.checkbox_tag = self.get_random_tag()
    self.mod_name_input_tag = self.get_random_tag()
    self.rows = 4
    self.cols = 3
    
    self.generator.add_modifier_changed_listener(self.update_table)

    self.create_window()
  

  def create_window(self):
    with dpg.window(label='XP Curve', tag=self.tag, show=True, pos=[20, 20], width=600, height=310, no_close=True):
      dpg.add_text('This table will update as you change the modifier.\nThe values shown will be the new requirements for each level.')
      dpg.add_separator()

      self.create_table()
      self.create_slider()
      self.create_checkbox()

      if self.generator.is_level_20:
        self.create_mod_name_input()
  

  def destroy(self):
    dpg.delete_item(self.tag)


  def create_table(self):
    with dpg.table(header_row=False, tag=self.table_tag):
      dpg.add_table_column()
      dpg.add_table_column()
      dpg.add_table_column()

      for row in range(self.rows):
        with dpg.table_row():
          for col in range(self.cols):
            cell = (row + (self.rows * col)) + 1

            if cell > 20:
              break

            dpg.add_input_int(
              label=f'Level {cell}',
              tag=f'{self.table_cell_tag}_{cell}',
              default_value=self.generator.custom_xp_curve[cell],
              min_value=1,
              min_clamped=True,
              max_value=999999999,
              max_clamped=True,
              callback=lambda id, value: self.generator.set_level_requirement(int(id.split('_')[-1]), value),
              on_enter=True,
              show=(not self.generator.is_level_20 and cell <= 12) or self.generator.is_level_20
            )

            if (not self.generator.is_level_20 and cell <= 12) or self.generator.is_level_20:
              # show default values in tooltips
              with dpg.tooltip(f'{self.table_cell_tag}_{cell}'):
                dpg.add_text(f'Default value: {self.generator.base_xp_curve[cell]}')
  

  def create_slider(self):
    dpg.add_slider_float(
      label='XP Modifier (?)',
      tag=self.modifier_slider_tag,
      default_value=1 / self.generator.xp_modifier,
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
  

  def create_checkbox(self):
    dpg.add_checkbox(
      label='Show level 20',
      tag=self.checkbox_tag,
      default_value=self.generator.is_level_20,
      callback=lambda: self.toggle_level_20()
    )


  def update_table(self):
    for row in range(self.rows):
      for col in range(self.cols):
        cell = (row + (self.rows * col)) + 1

        if cell > 20:
          break

        dpg.configure_item(f'{self.table_cell_tag}_{cell}', default_value=self.generator.custom_xp_curve[cell])


  def toggle_level_20(self):
    self.generator.set_is_level_20(not self.generator.is_level_20)
    self.rows = 7 if self.generator.is_level_20 else 4
    self.destroy()
    self.create_window()


  def create_mod_name_input(self):
    dpg.add_input_text(
      label='Level 20 Mod Name',
      tag=self.mod_name_input_tag,
      show=True,
      width=200,
      callback=lambda id, value: self.generator.set_mod_name(value)
    )

    with dpg.tooltip(self.mod_name_input_tag, tag=f'{self.mod_name_input_tag}_tooltip', show=True):
      dpg.add_text('''Enter the name of your mod here.
This will be used to create the correct folder structure for compatibility with your mod.
For example, if you use "UnlockLevelCurve", then that's what you should enter.
The name should match what you see in Vortex.
You MUST have a level 20 mod installed if you want to use a custom XP curve for levels 12+.
If you don't have a level 20 mod installed, you're gonna have a bad time.''')

