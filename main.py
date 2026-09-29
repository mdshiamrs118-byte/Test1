import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.uix.scrollview import ScrollView


class FileExplorer(BoxLayout):

  def __init__(self, **kwargs):
    super().__init__(orientation="vertical", spacing=10, padding=10, **kwargs)

    # Starting directory (Internal Storage root or current dir)
    self.current_path = "/sdcard" if os.path.exists("/sdcard") else "."

    # Current Path Header
    self.path_label = Label(
        text=self.current_path,
        size_hint_y=None,
        height=40,
        color=(0.2, 0.8, 1, 1),
        font_size="14sp",
    )
    self.add_widget(self.path_label)

    # Back / Up Directory Button
    self.up_btn = Button(
        text="⬆️ Go Up Directory",
        size_hint_y=None,
        height=45,
        background_color=(0.3, 0.3, 0.3, 1),
    )
    self.up_btn.bind(on_press=self.go_up)
    self.add_widget(self.up_btn)

    # Scrollable File List Container
    self.scroll_view = ScrollView()
    self.file_list = BoxLayout(
        orientation="vertical", size_hint_y=None, spacing=5
    )
    self.file_list.bind(minimum_height=self.file_list.setter("height"))
    self.scroll_view.add_widget(self.file_list)
    self.add_widget(self.scroll_view)

    # Load initial directory contents
    self.load_directory(self.current_path)

  def load_directory(self, path):
    self.current_path = path
    self.path_label.text = path
    self.file_list.clear_widgets()

    try:
      items = sorted(os.listdir(path))
    except PermissionError:
      self.file_list.add_widget(
          Label(text="Permission Denied!", size_hint_y=None, height=40)
      )
      return

    for item in items:
      full_path = os.path.join(path, item)
      is_dir = os.path.isdir(full_path)

      # Style folders differently from files
      display_name = f"📁 {item}" if is_dir else f"📄 {item}"
      btn = Button(
          text=display_name,
          size_hint_y=None,
          height=45,
          halign="left",
          valign="center",
          background_color=(0.15, 0.25, 0.4, 1)
          if is_dir
          else (0.2, 0.2, 0.2, 1),
      )
      btn.bind(
          on_press=lambda inst, p=full_path, d=is_dir: self.on_item_click(p, d)
      )
      self.file_list.add_widget(btn)

  def on_item_click(self, path, is_dir):
    if is_dir:
      self.load_directory(path)

  def go_up(self, instance):
    parent = os.path.dirname(self.current_path)
    if parent and parent != self.current_path:
      self.load_directory(parent)


class FileExplorerApp(App):

  def build(self):
    return FileExplorer()


if __name__ == "__main__":
  FileExplorerApp().run()
