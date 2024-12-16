from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

from custom_popup import ErrorPopup, SelectPopup
from db_interface import ResponseException, usersdbinterface
from folder_paths import GUI_folder, graphics_folder


Builder.load_file(GUI_folder + '/login_screen_GUI.kv')

# 로그인 입력창 클래스
class LoginWindow(BoxLayout):
    # 입력한 문자열이 유효한지 확인한 후에 로그인을 시도한다
    def login(self, *args):
        nickname = self.ids.nickname1.text
        password = self.ids.password1.text
        if nickname == "" or password == "":
            return
        result = usersdbinterface.login(nickname, password)
        if type(result) == ResponseException:
            if result.code == 401:
                SelectPopup('', 'Would you like to Sign up as a new account?', 'yes', 'no').open()
            else:
                ErrorPopup('Login error!', str(result)).open()
            return
        loginscreen.goto_post_screen()
loginwin = LoginWindow()

# 회원가입 입력창 클래스
# class SignupWindow(GridLayout):
#     # 입력한 문자열이 유효한지 확인한 후에 회원가입을 시도한다
#     def signup(self, *args):
#         nickname = self.ids.nickname2.text
#         mailaddr = self.ids.mailaddr.text
#         password = self.ids.password2.text
#         if self.isInvalidStr(nickname):
#             return
#         if self.isInvalidStr(mailaddr) or self.isInvalidMailaddr(mailaddr):
#             return
#         if self.isInvalidStr(password) or self.isDifferentPassword(password):
#             return
#         result = usersdbinterface.signup(nickname, mailaddr, password)
#         if type(result) == Popup:
#             result.open()
#             return
#         Popup(
#             title='Signup has succeeded!!',
#             content=Label(text='Now ye are our member! :)'),
#             size_hint=(1, 0.2),
#             auto_dismiss=True
#         ).open()
#     # 로그인 창으로 변경한다
#     def showLoginWin(self, *args):
#         loginscreen.showLoginWin(*args)
#     # 입력한 문자열이 유효한지 확인한다
#     def isInvalidStr(self, string):
#         if string.strip() in ['']:
#             Popup(
#                 title='Registration failed', 
#                 content=Label(text='Please input valid letter'),
#                 size_hint=(1, 0.2),
#                 auto_dismiss=True
#             ).open()
#             return True
#         else:
#             return False
#     # 입력한 메일주소가 유효한 형식인지 확인한다
#     def isInvalidMailaddr(self, mailaddr):
#         if not compile('[0-9A-Za-z]+@[0-9A-Za-z]+.[A-Za-z]+').match(mailaddr):
#             Popup(
#                 title='Registration failed', 
#                 content=Label(text='Please input valid format mail address'),
#                 size_hint=(1, 0.2),
#                 auto_dismiss=True
#             ).open()
#             return True
#         else:
#             return False
#     # 패스워드를 2번 입력할때 실수로 서로 똑같이 입력했는지 확인한다
#     def isDifferentPassword(self, password):
#         if password != self.ids.pswdagain.text:
#             Popup(
#                 title='Registration failed', 
#                 content=Label(text='Please input same password twice'),
#                 size_hint=(1, 0.2),
#                 auto_dismiss=True
#             ).open()
#             return True
#         else:
#             return False
# signupwin = SignupWindow()

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
loginscreen = LoginScreen(name="Login Screen")
