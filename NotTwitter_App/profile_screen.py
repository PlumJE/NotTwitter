from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from db_interface import ResponseException, userdetaildbinterface, usersdbinterface, postsdbinterface
from folder_paths import GUI_folder, graphics_folder
from common import PostUnit, redirection, AlertPopup


Builder.load_file(GUI_folder + '/profile_screen_GUI.kv')

# 누구에 관한 프로필인지 저장하는 상태 클래스
class ProfileWhom:
    __usernum = 0
    def get_usernum(self):
        return self.__usernum
    def set_usernum(self, usernum):
        self.__usernum = usernum
profilewhom = ProfileWhom()

# 최근 활동을 보여주는 스크린 클래스
class ProfileRecentScreen(Screen):
    # 초기 생성시 실행할 행동이다
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.on_pre_enter()
    # 게시글 스크린으로 들어가기 직전의 행동이다
    def on_pre_enter(self, *args):
        usernum = profilewhom.get_usernum()
        where = 'user.id = ' + str(usernum)
        order = 'posts.id'
        postlist = postsdbinterface.get_postlist(where, order)
        if type(postlist) == ResponseException:
            if postlist.code == 401:
                self.ids.recentlist.add_widget(PostUnit('', '', '', 'No recent activities.', lambda : None))
            else:
                AlertPopup('Adjust error!', str(postlist)).open()
            return
        self.ids.recentlist.clear_widgets()
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

# 상세 프로필을 보여주는 클래스
class ProfileDetailScreen(Screen):
    def on_pre_enter(self, *args):
        self.load_profile()
    def on_leave(self, *args):
        self.clean_profile()
    def hide_widget(self, widget):
        widget.size_hint = (None, None)
        widget.size = (0, 0)
        widget.opacity = 0
        widget.disabled = True
    def show_widget(self, widget):
        widget.size_hint = self.ids.phonelayout.size_hint
        widget.size = self.ids.phonelayout.size
        widget.opacity = 1
        widget.disabled = False
    def load_profile(self):
        userinfo = usersdbinterface.get_userinfo()
        if type(userinfo) == ResponseException:
            if userinfo.code != 401:
                AlertPopup('Load Error!', str(userinfo)).open()
                profilescreen.goto_post_screen()
            return
        
        self.ids.firstname.text = userinfo.get('firstname')
        self.ids.lastname.text = userinfo.get('lastname')
        self.ids.firstlogin.text = userinfo.get('firstlogin')
        self.ids.lastlogin.text = userinfo.get('lastlogin')

        userdetail = userdetaildbinterface.get_userdetail()
        if type(userdetail) == ResponseException:
            if userinfo.code != 401:
                AlertPopup('Load Error!', str(userdetail)).open()
                profilescreen.goto_post_screen()
            return
        
        self.ids.phone.text = userdetail.get('phone')
        self.ids.families.text = userdetail.get('families')
        self.ids.nation.text = userdetail.get('nation')
        self.ids.legion.text = userdetail.get('legion')
        self.ids.job.text = userdetail.get('job')
        self.ids.jobaddr.text = userdetail.get('jobaddr') 
    def save_profile(self):
        result = usersdbinterface.get_userinfo()
        if type(result) == ResponseException:
            AlertPopup('Save Error!', 'You need to save basic profile first!').open()
            return
        
        result = userdetaildbinterface.get_userdetail()
        if type(result) == ResponseException:
            AlertPopup('Save Error!', 'You need to save basic profile first!').open()
            return
        
        firstname = self.ids.firstname.text
        lastname = self.ids.lastname.text
        
        phone = self.ids.phone.text
        families = self.ids.families.text
        nation = self.ids.nation.text
        legion = self.ids.legion.text
        job = self.ids.job.text
        jobaddr = self.ids.jobaddr.text
        
        # result = usersdbinterface.put_userinfo(nickname, mailaddr, firstname, lastname)
        # if type(result) == ResponseException:
        #     AlertPopup('Save Error!', str(result)).open()
        #     return

        # result = userdetaildbinterface.put_userdetail(birth, phone, families, nation, legion, job, jobaddr)
        # if type(result) == ResponseException:
        #     AlertPopup('Save Error!', str(result)).open()
        #     return

        AlertPopup('', 'Profile Save Complete!').open()
    def clean_profile(self):
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

# 프로필 클래스
class ProfileScreen(Screen):
    bg_path = graphics_folder + '/post_background.jpg'
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.body.add_widget(profilerecentscreen)
        self.ids.body.add_widget(profiledetailscreen)
    def on_leave(self, *args):
        self.goto_profile_recent_screen()
    def register_mode(self, nickname, password):
        self.ids.nickname.text = nickname
        self.password = password
        self.register_mode = True
        self.ids.body.current = 'Profile Detail Screen'
    def save_basic_profile(self):
        nickname = self.ids.nickname.text
        mailaddr = self.ids.mailaddr.text
        birth = self.ids.birth.text
    def check_basic_profile(self):
        if self.ids.nickname.text == '':
            AlertPopup('', 'You must input pilsu info!')
            return False
        if self.ids.mailaddr.text == '':
            AlertPopup('', 'You must input pilsu info!')
            return False
        if self.ids.birth.text == '':
            AlertPopup('', 'You must input pilsu info!')
            return False
        return True
    def goto_profile_recent_screen(self):
        if not self.check_basic_profile():
            return
        self.ids.body.current = 'Profile Recent Screen'
    def goto_profile_detail_screen(self):
        if not self.check_basic_profile():
            return
        self.ids.body.current = 'Profile Detail Screen'
    def goto_post_screen(self):
        if not self.check_basic_profile():
            return
        self.manager.current = 'Post Screen'
profilescreen = ProfileScreen(name='Profile Screen')
