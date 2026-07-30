from pathlib import Path

from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

from logic import MemoryStore, process_text


class MemoryRow(BoxLayout):
    def __init__(self, store: MemoryStore, item: str, location: str, **kwargs):
        super().__init__(orientation="horizontal", size_hint_y=None, height=dp(42), spacing=dp(8), **kwargs)
        self.store = store
        self.item = item
        self.location = location

        self.add_widget(Label(text=item, halign="left", valign="middle"))
        self.add_widget(Label(text=location, halign="left", valign="middle"))

        btn = Button(text="Delete", size_hint_x=None, width=dp(90))
        btn.bind(on_press=self._delete)
        self.add_widget(btn)

    def _delete(self, *_):
        _ = self.store.retrieve_and_delete(self.item)
        self.parent.parent.refresh_list()


class RootWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", spacing=dp(8), padding=dp(10), **kwargs)
        self.store = MemoryStore("android_memories.db")

        self.status = Label(text="Type: I put the key in drawer / Where is the key?", size_hint_y=None, height=dp(48))
        self.add_widget(self.status)

        self.input_box = TextInput(hint_text="Enter command...", multiline=False, size_hint_y=None, height=dp(48))
        self.add_widget(self.input_box)

        row = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(8))
        save_btn = Button(text="Save / Ask")
        list_btn = Button(text="List")
        clear_btn = Button(text="Clear")
        save_btn.bind(on_press=self.on_process)
        list_btn.bind(on_press=self.refresh_list)
        clear_btn.bind(on_press=self.on_clear)
        row.add_widget(save_btn)
        row.add_widget(list_btn)
        row.add_widget(clear_btn)
        self.add_widget(row)

        self.scroll = ScrollView()
        self.list_box = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(6), padding=(0, dp(4)))
        self.list_box.bind(minimum_height=self.list_box.setter("height"))
        self.scroll.add_widget(self.list_box)
        self.add_widget(self.scroll)

        Clock.schedule_once(lambda *_: self.refresh_list())

    def on_process(self, *_):
        cmd = self.input_box.text.strip()
        if not cmd:
            self.status.text = "Please type something first."
            return
        response = process_text(cmd, self.store)
        self.status.text = response
        self.input_box.text = ""
        self.refresh_list()

    def refresh_list(self, *_):
        self.list_box.clear_widgets()
        rows = self.store.list_all()
        if not rows:
            self.list_box.add_widget(Label(text="No memories saved yet.", size_hint_y=None, height=dp(30)))
            return
        for item, loc in rows:
            self.list_box.add_widget(MemoryRow(self.store, item, loc))

    def on_clear(self, *_):
        self.input_box.text = ""
        self.status.text = "Cleared."

    def close(self):
        self.store.close()


class AndroidReminderApp(App):
    def build(self):
        self.title = "Memory Reminder"
        self.root_widget = RootWidget()
        return self.root_widget

    def on_stop(self):
        if hasattr(self, "root_widget"):
            self.root_widget.close()


if __name__ == "__main__":
    AndroidReminderApp().run()

