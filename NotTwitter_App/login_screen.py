from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

from profile_screen import profilescreen
from db_interface import usersdbinterface, userdetaildbinterface
from folder_paths import GUI_folder, graphics_folder
from common import AlertPopup, InsertPopup


Builder.load_file(GUI_folder + '/login_screen_GUI.kv')

# 로그인 입력창 클래스
class LoginWindow(BoxLayout):
    # 입력한 문자열이 유효한지 확인한 후에 로그인을 시도한다
    def login(self, *args):
        nickname = self.ids.nickname.text
        mailaddr = self.ids.mailaddr.text
        password = self.ids.password.text

        if not nickname or not mailaddr or not password:
            return

        result = usersdbinterface.login(nickname, mailaddr, password)
        if result is None:
            return
        elif result == 0:
            InsertPopup('Are you first time?', 'If you wanna sign-up as new user,\n please insert password again.', self.register, True).open()
        else:
            loginscreen.goto_post_screen()
    def register(self, password_again):
        nickname = self.ids.nickname.text
        mailaddr = self.ids.mailaddr.text
        password = self.ids.password.text

        if password != password_again:
            AlertPopup('Register Error!', 'The password does not match').open()
            return

        result = usersdbinterface.post_userinfo(nickname, mailaddr, password)
        if not result:
            return
        print('post_userinfo 성공')

        usernum = usersdbinterface.login(nickname, mailaddr, password)
        if not usernum:
            return
        print('login 성공')

        result = userdetaildbinterface.post_userdetail(usernum)
        if not result:
            # 로그아웃을 계속 시도한다
            while not usersdbinterface.logout():
                pass
            return
        print('post_userdetail 성공')

        AlertPopup('', 'Sign in succeeded!').open()
        loginscreen.goto_post_screen()
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
    # 프로필 스크린으로 들어간다(회원가입 이후)
    def goto_profile_screen(self):
        self.manager.current = 'Profile Screen'
        profilescreen.ids.body.current = 'Profile Detail Screen'
loginscreen = LoginScreen(name="Login Screen")
