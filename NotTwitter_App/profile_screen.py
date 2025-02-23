from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from db_interface import ResponseException, userdetaildbinterface, usersdbinterface, postsdbinterface
from folder_paths import GUI_folder, graphics_folder
from common import PostUnit, ClickableImg, redirection, AlertPopup, InsertPopup, FileChooserPopup


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
        # 부모 스크린이 나타나기 직전 같이 실행될 행동
    def on_parent_enter(self):
        self.on_pre_enter()
    # 부모 스크린이 사라진 직후 같이 실행될 행동
    def on_parent_leave(self):
        pass
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
        if postlist is None:
            return
        
        if len(postlist) == 0:
            self.ids.recentlist.add_widget(PostUnit('', None, None, 'There\'s no recent activities.', None))
            return

        for post in postlist:
            result = postsdbinterface.get_post(post)
            if result is None:
                return

            id = result.get('id')
            writernum = result.get('writer')
            userinfo = usersdbinterface.get_userinfo(writernum)
            if userinfo is None:
                return

            writer = userinfo.get('nickname')
            writedate = result.get('writedate')
            content = result.get('content')
            action = lambda id=id : self.redirect(id)

            profile_url = userdetaildbinterface.download_profile(writernum)
            if profile_url:
                profileimg = ClickableImg(
                    profile_url,
                    lambda : None,
                    size_hint=(0.9, 0.9)
                )
            else:
                profileimg = None
            
            postimg_url = postsdbinterface.download_postimg(id)
            if postimg_url:
                postimg = ClickableImg(
                    postimg_url,
                    lambda : None
                )
            else:
                postimg = None

            self.ids.recentlist.add_widget(PostUnit(id, writer, writedate, content, action, profileimg, postimg))
    # 리다이렉션한다
    def redirect(self, id):
        redirection.set_redirection(id)
        profilescreen.goto_post_screen()
profilerecentscreen = ProfileRecentScreen(name='Profile Recent Screen')

# 상세 프로필을 보여주는 스크린 클래스
class ProfileDetailScreen(Screen):
    # 부모 스크린이 나타나기 직전 같이 실행될 행동
    def on_parent_enter(self):
        # profilewhom의 usernum이 None이 아니면, Change버튼을 숨긴다다.
        if profilewhom.get_usernum is not None:
            self.showhide_changeBtn(show=False)
            self.readonly_profiles(readonly=True)
        self.load_profile()
    # 부모 스크린이 사라진 직후 같이 실행될 행동
    def on_parent_leave(self):
        self.showhide_changeBtn(show=True)
        self.readonly_profiles(readonly=False)
    # 스크린이 나타나기 직전 행동
    def on_pre_enter(self, *args):
        self.load_profile()
    # 스크린이 사라진 직후 행동
    def on_leave(self, *args):
        self.clean_profile()
    # Change버튼을 숨기거나 드러낸다
    def showhide_changeBtn(self, show):
        self.changeBtn_size_hint = self.ids.changeBtn.size_hint
        self.changeBtn_size = self.ids.changeBtn.size
        self.ids.changeBtn.size_hint = self.changeBtn_size_hint if show else (None, None)
        self.ids.changeBtn.size = self.changeBtn_size if show else (0, 0)
        self.ids.changeBtn.opacity = 1 if show else 0
        self.ids.changeBtn.disabled = False if show else True
    # 프로필들 readonly설정을 on/off한다
    def readonly_profiles(self, readonly):
        self.ids.nickname.readonly = True if readonly else False
        self.ids.mailaddr.readonly = True if readonly else False
        self.ids.birth.readonly = True if readonly else False
        self.ids.firstname.readonly = True if readonly else False
        self.ids.lastname.readonly = True if readonly else False
        self.ids.phone.readonly = True if readonly else False
        self.ids.families.readonly = True if readonly else False
        self.ids.nation.readonly = True if readonly else False
        self.ids.legion.readonly = True if readonly else False
        self.ids.job.readonly = True if readonly else False
        self.ids.jobaddr.readonly = True if readonly else False
    # DB에서 프로필을 불러온다
    def load_profile(self):
        # profilewhom의 usernum이 None이면, 자신의 유저번호를 가져온다.
        usernum = profilewhom.get_usernum()
        if usernum is None:
            usernum = usersdbinterface.usernum

        userinfo = usersdbinterface.get_userinfo(usernum)
        if type(userinfo) == ResponseException:
            if userinfo.code != 401:
                AlertPopup('Load Error!', str(userinfo)).open()
                profilescreen.goto_post_screen()
            return
        
        userdetail = userdetaildbinterface.get_userdetail(usernum)
        if userdetail is None:
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

        self.former_nickname = self.ids.nickname.text
        self.former_mailaddr = self.ids.mailaddr.text

        profilescreen.ids.nickname.text = self.ids.nickname.text
        profilescreen.ids.mailaddr.text = 'Mail address : \n' + self.ids.mailaddr.text
        profilescreen.ids.birth.text = 'Birth Date : \n' + self.ids.birth.text
    # DB에 변경한 프로필을 저장하기 전 행동이다
    def change_profile(self):
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

        result = usersdbinterface.login(self.former_nickname, self.former_mailaddr, password)
        if result is None:
            return

        result = usersdbinterface.put_userinfo(nickname, mailaddr, firstname, lastname)
        if result is None:
            return
        
        result = userdetaildbinterface.put_userdetail(birth, phone, families, nation, legion, job, jobaddr)
        if result is None:
            return
        
        AlertPopup('', 'Profile Change Complete!').open()
        self.load_profile()
        profilescreen.update_profile()
    # 프로필 리스트를 초기화시킨다
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
        self.filechooser = FileChooserPopup('Select Image', self.update_pfimg)
    # 들어올 때 행동
    def on_pre_enter(self, *args):
        profilerecentscreen.on_parent_enter()
        profiledetailscreen.on_parent_enter()
        self.update_profile()
    # 떠날 때 행동
    def on_leave(self, *args):
        profilerecentscreen.on_parent_leave()
        profiledetailscreen.on_parent_leave()
        self.goto_profile_recent_screen()
    # 헤더를 업데이트 한다
    def update_profile(self):
        usernum = profilewhom.get_usernum()
        
        profileimg = ClickableImg(
            userdetaildbinterface.download_profile(usernum),
            lambda : self.filechooser.open(),
            size_hint=(0.9, 0.9)
        )

        self.ids.pfimg_layout.clear_widgets()
        self.ids.pfimg_layout.add_widget(profileimg)
    # 프로필 사진을 업데이트한다
    def update_pfimg(self, paths):
        userdetaildbinterface.upload_profile(paths[0])
        self.update_profile()
    # 최근 활동 스크린을 불러온다
    def goto_profile_recent_screen(self):
        if not usersdbinterface.usernum:
            return
        self.ids.body.current = 'Profile Recent Screen'
    # 프로필 상세보기 및 편집 스크린을 불러온다
    def goto_profile_detail_screen(self):
        if not usersdbinterface.usernum:
            return
        self.ids.body.current = 'Profile Detail Screen'
    # 게시글 스크린으로 간다
    def goto_post_screen(self):
        if not usersdbinterface.usernum:
            return
        self.manager.current = 'Post Screen'
profilescreen = ProfileScreen(name='Profile Screen')
