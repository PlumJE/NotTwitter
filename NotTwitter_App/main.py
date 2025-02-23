"""
작성자 : 외기러기
작성시작일 : 2024-03-05
버전 정보 : 1.0.0 at 2025-02-23
내가 만든 이 코드를 당신 또는 다른사람이 먼저 만들었다고 거짓말하지 마세요!!
"""

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

from login_screen import loginscreen
from post_screen import postscreen
from edit_screen import editscreen
from profile_screen import profilescreen
from menu_screen import menuscreen


Window.clearcolor = (1, 1, 1, 1)
Window.size = (350, 750)

class NotTwitterApp(App):
    screen_manager = ScreenManager()
    # 앱 전체를 만들어서 리턴한다
    def build(self):
        self.screen_manager.add_widget(loginscreen)
        self.screen_manager.add_widget(postscreen)
        self.screen_manager.add_widget(editscreen)
        self.screen_manager.add_widget(profilescreen)
        self.screen_manager.add_widget(menuscreen)
        return self.screen_manager

if __name__ == "__main__":
    NotTwitterApp().run()