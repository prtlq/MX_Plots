from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle
import logging
from subs import AppInteraction, ExecuteFunctions

logging.basicConfig(filename='app.log', level=logging.DEBUG)

try:
    Config.set('graphics', 'width', '300')
    Config.set('graphics', 'height', '600')

    def execute_action(instance, file_chooser, result_label, toggle_button):
        mode = toggle_button.text
        ExecuteFunctions.execute_action(file_chooser, result_label, mode)

    def toggle_action(instance):
        AppInteraction.toggle_action(instance)

    class mxPlots(App):
        def build(self):
            with Window.canvas.before:
                Color(0.2, 0.2, 0.2, 1)
                self.rect = Rectangle(size=Window.size, pos=(0, 0))

            layout = AnchorLayout(anchor_x='center', anchor_y='center')
            content_layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

            file_chooser = FileChooserListView(path='.')

            toggle_button = ToggleButton(text="Batch Mode", state='down', group="mode_toggle", background_color=(0.4, 0.4, 0.4, 1), size_hint=(None, None), size=(150, 40))
            toggle_button.bind(on_press=toggle_action)

            execute_button = Button(text="Execute", background_color=(0.6, 0.6, 0.6, 1), size_hint_y=None, height=50)
            execute_button.bind(on_press=lambda instance: execute_action(instance, file_chooser, result_label, toggle_button))

            button_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
            button_layout.add_widget(toggle_button)
            button_layout.add_widget(execute_button)

            content_layout.add_widget(file_chooser)
            content_layout.add_widget(button_layout)

            tab_panel = TabbedPanel(do_default_tab=False)
            tab1 = TabbedPanelItem(text='Main')
            tab1.add_widget(content_layout)

            tab2 = TabbedPanelItem(text='Settings')
            settings_message = Label(text="This is the Landing/settings page.", color=(1, 1, 1, 1))
            tab2.add_widget(settings_message)

            tab_panel.add_widget(tab1)
            tab_panel.add_widget(tab2)

            result_label = Label(text="", color=(1, 1, 1, 1), size_hint_y=None, height=50)
            content_layout.add_widget(result_label)

            layout.add_widget(tab_panel)
            return layout

    if __name__ == "__main__":
        mxPlots().run()

except Exception as e:
    logging.exception("Exception occurred")
