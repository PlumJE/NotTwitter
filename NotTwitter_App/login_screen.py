from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

from profile_screen import profilescreen
from db_interface import ResponseException, usersdbinterface
from folder_paths import GUI_folder, graphics_folder
from common import AlertPopup, SelectPopup


Builder.load_file(GUI_folder + '/login_screen_GUI.kv')

# 로그인 입력창 클래스
class LoginWindow(BoxLayout):
    # 입력한 문자열이 유효한지 확인한 후에 로그인을 시도한다
    async def login(self, *args):
        nickname = self.ids.nickname.text
        password = self.ids.password.text
        if nickname == "" or password == "":
            return

        result = await usersdbinterface.login(nickname, password)
        if type(result) == ResponseException:
            if result.code == 401:
                popup = SelectPopup('First time?', 'We\'ve never seen you before.\nWould you like to sign up as a new account?', 'yes', 'no')
                await popup.open()
                print(popup.get_result())
                if popup.get_result():
                    self.register()
            else:
                AlertPopup('Login error!', str(result)).open()
            return
        loginscreen.goto_post_screen()
    def register(self):
        nickname = self.ids.nickname.text
        password = self.ids.password.text

        loginscreen.goto_profile_screen()
        profilescreen.goto_profile_detail_screen()
        profilescreen.register_mode(nickname, password)
loginwin = LoginWindow()

# 로그인 스크린 클래스
class LoginScreen(Screen):
    # state가 0이면 아무런 창도 없고, 1이면 로그인 창만, 2이면 회원가입 창만 있는 상태
    state = 0
    bg_path = graphics_folder + '/login_background.jpg'
    # 로그인 창을 연다
    def openLoginWin(self, *args):
        if self.state == 0:
            self.state = 1
            self.ids.loginlayout.add_widget(loginwin)
    # 게시글 스크린으로 들어간다
    def goto_post_screen(self):
        self.manager.current = "Post Screen"
    # 프로필 스크린으로 들어간다(회원가입용)
    def goto_profile_screen(self):
        self.manager.current = 'Profile Screen'
loginscreen = LoginScreen(name="Login Screen")
