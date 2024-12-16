from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

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

        if yesFunc == None:
            yesFunc = lambda x: None
        if noFunc == None:
            noFunc = self.dismiss

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