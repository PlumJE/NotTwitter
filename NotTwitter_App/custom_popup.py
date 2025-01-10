from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

class ErrorPopup(Popup):
    def __init__(self, title, content, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.content = Label(text=content)
        self.size_hint=(1, 0.2)
        self.auto_dismiss=True

class SelectPopup(Popup):
    def __init__(self, title, content, yesText, noText, yesFunc=None, noFunc=None, **kwargs):
        super().__init__(**kwargs)

        yesFunc = self.click_template(yesFunc)
        noFunc = self.click_template(noFunc)

        innerLayout1 = BoxLayout()
        innerLayout1.add_widget(Label(text=content))

        innerLayout2 = BoxLayout(orientation='horizontal')
        innerLayout2.add_widget(Button(text=yesText, on_release=yesFunc))
        innerLayout2.add_widget(Button(text=noText, on_release=noFunc))

        contentLayout = BoxLayout(orientation='vertical')
        contentLayout.add_widget(innerLayout1)
        contentLayout.add_widget(innerLayout2)

        self.title=title
        self.content=contentLayout
        self.size_hint=(1, 0.2)
        self.auto_dismiss=True
    def click_template(self, func):
        def template(*args):
            if func != None:
                func(*args)
            self.dismiss()
        return template
    
class InsertPopup(Popup):
    _value = None
    _textInput = TextInput()
    def __init__(self, title, **kwargs):
        super().__init__(**kwargs)

        contentLayout = BoxLayout(orientation='vertical')
        contentLayout.add_widget(self._textInput)
        contentLayout.add_widget(Button(text='Input!', on_release=self._setValue))

        self.title=title
        self.content=contentLayout
        self.size_hint=(1, 0.2)
        self.auto_dismiss=True
