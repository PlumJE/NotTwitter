from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from db_interface import ResponseException, userdetaildbinterface, usersdbinterface, postsdbinterface
from folder_paths import GUI_folder, graphics_folder
from common import PostUnit, redirection, AlertPopup, InsertPopup


Builder.load_file(GUI_folder + '/profile_screen_GUI.kv')

# 누구에 관한 프로필인지 저장하는 클래스
class ProfileWhom:
    __usernum = None
    __nickname = None
    __password = None
    def set_usernum(self, usernum):
        self.__usernum = usernum
        self.__nickname = None
        self.__password = None
    def set_nickname_password(self, nickname, password):
        self.__usernum = None
        self.__nickname = nickname
        self.__password = password
    def clear_all(self):
        self.__usernum = None
        self.__nickname = None
        self.__password = None
    def get_usernum(self):
        return self.__usernum
    def get_nickname(self):
        return self.__nickname
    def get_password(self):
        return self.__password
profilewhom = ProfileWhom()

# 최근 활동을 보여주는 스크린 클래스
class ProfileRecentScreen(Screen):
    # 초기 생성시 실행할 행동이다
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.on_pre_enter()
    # 스크린이 나타나기 직전 행동
    def on_pre_enter(self, *args):
        self.ids.recentlist.clear_widgets()
        self.load_users_post()
    # 유저가 게시한 글을 보여준다
    def load_users_post(self):
        # usernum이 주어지지 않으면 현재 유저, 값이 주어지면 해당 유저의 번호를 저장한다
        usernum = profilewhom.get_usernum()
        usernum = usernum if usernum else usersdbinterface.get_header().get('usernum')
        where = 'user.id = ' + str(usernum)
        order = 'posts.id'

        # 유저 번호에 해당하는 유저의 게시글만 가져온다
        postlist = postsdbinterface.get_postlist(where, order)
        if type(postlist) == ResponseException:
            AlertPopup('Post loading error!', str(postlist)).open()
            return
        
        for post in postlist:
            result = postsdbinterface.get_post(post)
            if type(result) == ResponseException:
                AlertPopup('Adjust error!', str(result)).open()
                return
            id = result.get('id')
            writer = result.get('writer')
            userinfo = usersdbinterface.get_userinfo(writer)
            if type(userinfo) == ResponseException:
                AlertPopup('Adjust error!', str(userinfo)).open()
                return
            writer = userinfo.get('nickname')
            writedate = result.get('writedate')
            content = result.get('content')
            action = lambda id=id : self.redirect(id)
            self.ids.recentlist.add_widget(PostUnit(id, writer, writedate, content, action))
    # 리다이렉션한다
    def redirect(self, id):
        redirection.set_redirection(id)
        profilescreen.goto_post_screen()
profilerecentscreen = ProfileRecentScreen(name='Profile Recent Screen')

# 상세 프로필을 보여주는 스크린 클래스
class ProfileDetailScreen(Screen):
    # 부모 스크린이 나타나기 직전 같이 실행될 행동
    def on_parent_enter(self):
        if not usersdbinterface.is_login():
            self.hide_widget(self.ids.firstloginlayout)
            self.hide_widget(self.ids.lastloginlayout)
        self.load_profile()
    # 부모 스크린이 사라진 직후 같이 실행될 행동
    def on_parent_leave(self):
        self.show_widget(self.ids.firstloginlayout)
        self.show_widget(self.ids.lastloginlayout)
    # 스크린이 나타나기 직전 행동
    def on_pre_enter(self, *args):
        self.load_profile()
    # 스크린이 사라진 직후 행동
    def on_leave(self, *args):
        self.clean_profile()
    # 위젯을 숨긴다
    def hide_widget(self, widget):
        widget.size_hint = (None, None)
        widget.size = (0, 0)
        widget.opacity = 0
        widget.disabled = True
    # 위젯을 보여준다
    def show_widget(self, widget):
        widget.size_hint = self.ids.phonelayout.size_hint
        widget.size = self.ids.phonelayout.size
        widget.opacity = 1
        widget.disabled = False
    # DB에서 프로필을 불러온다
    def load_profile(self):
        if not usersdbinterface.is_login():
            self.ids.nickname.text = profilewhom.get_nickname()
            return

        usernum = profilewhom.get_usernum()

        userinfo = usersdbinterface.get_userinfo(usernum)
        if type(userinfo) == ResponseException:
            if userinfo.code != 401:
                AlertPopup('Load Error!', str(userinfo)).open()
                profilescreen.goto_post_screen()
            return
        
        userdetail = userdetaildbinterface.get_userdetail(usernum)
        if type(userdetail) == ResponseException:
            if userinfo.code != 401:
                AlertPopup('Load Error!', str(userdetail)).open()
                profilescreen.goto_post_screen()
            return
        
        self.ids.nickname.text = userinfo.get('nickname')
        self.ids.mailaddr.text = userinfo.get('mailaddr')
        self.ids.birth.text = userdetail.get('birth')

        self.ids.firstname.text = userinfo.get('firstname')
        self.ids.lastname.text = userinfo.get('lastname')
        self.ids.firstlogin.text = userinfo.get('firstlogin')
        self.ids.lastlogin.text = userinfo.get('lastlogin')
        self.ids.phone.text = userdetail.get('phone')
        self.ids.families.text = userdetail.get('families')
        self.ids.nation.text = userdetail.get('nation')
        self.ids.legion.text = userdetail.get('legion')
        self.ids.job.text = userdetail.get('job')
        self.ids.jobaddr.text = userdetail.get('jobaddr')
    # DB에 변경한 프로필을 저장하기 전 행동이다
    def save_profile(self):
        nickname = self.ids.nickname.text
        mailaddr = self.ids.mailaddr.text
        birth = self.ids.birth.text

        if not nickname or not mailaddr or not birth:
            AlertPopup('Input Error!', 'Please input essential infomations').open()
            return
        
        InsertPopup('Authentication', "Please enter the password again", self.__save_profile, True).open()
    # DB에 변경한 프로필을 저장한다
    def __save_profile(self, password):
        nickname = self.ids.nickname.text
        mailaddr = self.ids.mailaddr.text
        birth = self.ids.birth.text

        firstname = self.ids.firstname.text
        lastname = self.ids.lastname.text
        phone = self.ids.phone.text
        families = self.ids.families.text
        nation = self.ids.nation.text
        legion = self.ids.legion.text
        job = self.ids.job.text
        jobaddr = self.ids.jobaddr.text

        if not usersdbinterface.is_login():
            if profilewhom.get_password() != password:
                AlertPopup('Register error!', 'Please insert right password').open()
                return
            
            result = usersdbinterface.post_userinfo(nickname, password, mailaddr, firstname, lastname)
            if type(result) == ResponseException:
                AlertPopup('Register error!', str(result)).open()
                return
            
            result = usersdbinterface.login(nickname, password)
            if type(result) == ResponseException:
                AlertPopup('Register error!', str(result)).open()
                return
            
            result = userdetaildbinterface.post_userdetail(birth, phone, families, nation, legion, job, jobaddr)
            if type(result) == ResponseException:
                AlertPopup('Register error!', str(result)).open()
                usersdbinterface.logout()
                return
            
            profilewhom.clear_all()
            AlertPopup('Register Complete!', 'Welcome and Enjoy my App~').open()
        else:
            result = usersdbinterface.login(nickname, password)
            if type(result) == ResponseException:
                AlertPopup('Update error!', 'Please insert right password').open()
                return

            result = usersdbinterface.put_userinfo(nickname, mailaddr, firstname, lastname)
            if type(result) == ResponseException:
                AlertPopup('Update error!', str(result)).open()
                return
            
            result = userdetaildbinterface.put_userdetail(birth, phone, families, nation, legion, job, jobaddr)
            if type(result) == ResponseException:
                AlertPopup('Update error!', str(result)).open()
                usersdbinterface.logout()
                return
            
            AlertPopup('', 'Profile Save Complete!').open()
        self.load_profile()
        profilescreen.update_profile()
    # 프로필 리스트를 초기화시킨다다
    def clean_profile(self):
        self.ids.nickname.text = ''
        self.ids.mailaddr.text = ''
        self.ids.birth.text = ''

        self.ids.firstname.text = ''
        self.ids.lastname.text = ''
        self.ids.firstlogin.text = ''
        self.ids.lastlogin.text = ''
        self.ids.phone.text = ''
        self.ids.families.text = ''
        self.ids.nation.text = ''
        self.ids.legion.text = ''
        self.ids.job.text = ''
        self.ids.jobaddr.text = ''
profiledetailscreen = ProfileDetailScreen(name='Profile Detail Screen')

# 프로필 스크린 클래스
class ProfileScreen(Screen):
    bg_path = graphics_folder + '/post_background.jpg'
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.body.add_widget(profilerecentscreen)
        self.ids.body.add_widget(profiledetailscreen)
    # 들어올 때 행동
    def on_pre_enter(self, *args):
        profiledetailscreen.on_parent_enter()
    # 떠날 때 행동
    def on_leave(self, *args):
        self.goto_profile_recent_screen()
        profiledetailscreen.on_parent_leave()
    # 헤더를 업데이트 한다
    def update_profile(self):
        userinfo = usersdbinterface.get_userinfo()
        if type(userinfo) == ResponseException:
            if userinfo.code != 401:
                AlertPopup('Load Error!', str(userinfo)).open()
                profilescreen.goto_post_screen()
            return
        
        userdetail = userdetaildbinterface.get_userdetail()
        if type(userdetail) == ResponseException:
            if userinfo.code != 401:
                AlertPopup('Load Error!', str(userdetail)).open()
                profilescreen.goto_post_screen()
            return
        
        self.ids.nickname.text = userinfo.get('nickname')
        self.ids.mailaddr.text = 'Mail address : ' + userinfo.get('mailaddr')
        self.ids.birth.text = 'Birth date : ' + userdetail.get('birth')
    # 회원가입을 준비한다
    def register_ready(self, nickname, password):
        profilewhom.set_nickname_password(nickname, password)
        self.ids.body.current = 'Profile Detail Screen'
    # 최근 활동 스크린을 불러온다
    def goto_profile_recent_screen(self):
        if not usersdbinterface.is_login():
            return
        self.ids.body.current = 'Profile Recent Screen'
    # 프로필 상세보기 및 편집 스크린을 불러온다
    def goto_profile_detail_screen(self):
        if not usersdbinterface.is_login():
            return
        self.ids.body.current = 'Profile Detail Screen'
    # 게시글 스크린으로 간다다
    def goto_post_screen(self):
        if not usersdbinterface.is_login():
            return
        self.manager.current = 'Post Screen'
profilescreen = ProfileScreen(name='Profile Screen')
