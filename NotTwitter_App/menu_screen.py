from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from db_interface import usersdbinterface
from folder_paths import GUI_folder, graphics_folder


Builder.load_file(GUI_folder + '/menu_screen_GUI.kv')

# 환경설정 스크린 클래스
class SettingScreen(Screen):
    bg_path = graphics_folder + '/post_background.jpg'
    # 환경설정 스크린으로 들어가기 직전의 행동이다
    def on_pre_enter(self, *args):
        self.ids.usernum.text = usersdbinterface.get_header().get('usernum')
    # 로그아웃 한다
    def logout(self, *args):
        usersdbinterface.logout()
        self.goto_login_screen()
    # 게시글 스크린으로 들어간다
    def goto_post_screen(self):
        self.manager.current = 'Post Screen'
    # 로그인 스크린으로 들어간다
    def goto_login_screen(self):
        self.manager.current = 'Login Screen'
menuscreen = SettingScreen(name='Menu Screen')

# class MenuScreen(Screen):
#     bg_path = graphics_folder + '/post_background.jpg'
#     screen_manager = ScreenManager()
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.screen_manager.add_widget(SettingScreen(name='Setting Screen'))
#     def goto_login_screen(self):
#         self.manager.current = 'Login Screen'
#     def goto_post_screen(self):
#         self.manager.current = 'Post Screen'
# menuscreen = MenuScreen(name='Menu Screen')