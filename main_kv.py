from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserListView


class TestScreen(GridLayout):

    def test_call(self, btn_obj, **kwargs):
        print('self:', self)
        print('btn_obj:', btn_obj)
        print('**kwargs:', **kwargs)
        self.result_field.text = f"{self.drawer.path} {self.drawer.selection}"

    def __init__(self, **kwargs):
        super(TestScreen, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text='Name'))
        self.name_field = TextInput(multiline=False)
        self.add_widget(self.name_field)
        self.add_widget(Label(text='Password'))
        self.password_field = TextInput(password=True, multiline=False)
        self.add_widget(self.password_field)
        self.button = Button(text='Pass')
        self.button.bind(on_press=self.test_call)
        self.add_widget(self.button)
        self.result_field = Label()
        self.add_widget(self.result_field)
        self.image_field = Image()
        self.add_widget(self.image_field)
        self.drawer = FileChooserListView(path='~')
        self.add_widget(self.drawer)


class MainApp(App):

    def build(self):
        return TestScreen()


if __name__ == "__main__":
    MainApp().run()
