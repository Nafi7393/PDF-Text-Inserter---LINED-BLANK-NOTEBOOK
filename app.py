from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.progressbar import MDProgressBar
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivymd.theming import ThemeManager
from main import add_lines_to_pdf


class PDFApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.run_btn = None
        self.file_btn = None
        self.text_field = None
        self.title = "PDF App"
        self.screen = Screen()
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path
        )
        self.theme_cls = ThemeManager()
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Light"
        self.progress_bar = None

    def build(self):
        layout = MDBoxLayout(orientation='vertical', spacing=10, padding=40)

        label = MDLabel(text="PDF App", halign='center', font_style='H3')
        layout.add_widget(label)

        self.text_field = MDTextField(
            hint_text="Enter the path of the text file",
            mode="rectangle"
        )
        layout.add_widget(self.text_field)

        self.file_btn = MDRaisedButton(
            text="Open File Manager",
            on_release=self.open_file_manager,
            pos_hint={'center_x': 0.5}
        )
        layout.add_widget(self.file_btn)

        self.run_btn = MDRaisedButton(
            text="Run",
            on_release=self.run_function,
            pos_hint={'center_x': 0.5}
        )
        layout.add_widget(self.run_btn)
        self.screen.add_widget(layout)

        return self.screen

    def open_file_manager(self, obj):
        self.file_manager.show('/')

    def exit_manager(self, *args):
        self.file_manager.close()

    def select_path(self, path):
        self.text_field.text = path
        self.exit_manager()

    def run_function(self, obj):
        text_file_path = self.text_field.text

        if not text_file_path:
            dialog = MDDialog(title="Error", text="Please enter the path of the text file")
            dialog.open()
            return

        def target_func():
            add_lines_to_pdf(
                input_pdf_path='109 Page Lined.pdf',
                output_pdf_path='INTERIOR.pdf',
                text_file_path=text_file_path
            )
            self.progress_bar.value = 100
            self.show_success_dialog()

        self.progress_bar.value = 50
        target_func()

    @staticmethod
    def show_success_dialog():
        dialog = MDDialog(title="Success", text="PDF Generation Successful!")
        dialog.open()


if __name__ == "__main__":
    Window.size = (360, 640)
    PDFApp().run()
