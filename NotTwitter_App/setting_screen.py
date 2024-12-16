from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen

from db_interface import usersdbinterface, postsdbinterface
from folder_paths import GUI_folder, graphics_folder
from debug import logger

Builder.load_file(GUI_folder + '/setting_screen_GUI.kv')

# 닉네임 바꾸게 도와주는 팝업 클래스
class ChangeNickPopup(Popup):
    # 현재 유저의 닉네임을 입력해 팝업을 생성한다
    def __init__(self, cur_nick, **kwargs):
        super().__init__(**kwargs)
        self.ids.new_nick.text = cur_nick
    # 닉네임을 검토한 뒤 변경을 승인한다
    def adjust(self, *args):
        new_nick = self.ids.new_nick.text
        usersdbinterface.put_userinfo(new_nick)
        settingscreen.update_userinfo()
        logger.info('Changing nickname succeed!')
        self.dismiss()
    # 닉네임 변경을 포기한다
    def discard(self, *args):
        self.dismiss()

# 환경설정 스크린 클래스
class SettingScreen(Screen):
    bg_path = graphics_folder + '/post_background.jpg'
    # 환경설정 스크린으로 들어가기 직전의 행동이다
    def on_pre_enter(self, *args):
        self.ids.nickname.text = usersdbinterface.get_userinfo().get('nickname')
        self.ids.usernum.text = usersdbinterface.get_header().get('usernum')
    # 닉네임 변경하는 팝업창을 띄운다
    def change_nick(self, *args):
        ChangeNickPopup(self.ids.nickname.text).open()
    # 닉네임을 갱신한다
    def update_userinfo(self):
        self.ids.nickname.text = usersdbinterface.get_userinfo()
    # 로그아웃 한다
    def logout(self, *args):
        usersdbinterface.logout()
        self.goto_login_screen()
    # 뒤로 돌아간다
    def exit(self, *args):
        self.goto_post_screen()
    # 게시글 스크린으로 들어간다
    def goto_post_screen(self):
        self.manager.current = 'Post Screen'
    # 로그인 스크린으로 들어간다
    def goto_login_screen(self):
        self.manager.current = 'Login Screen'
settingscreen = SettingScreen(name='Setting Screen')