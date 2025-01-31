from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.behaviors import ButtonBehavior

from profile_screen import profilewhom
from db_interface import ResponseException, usersdbinterface, postsdbinterface
from folder_paths import GUI_folder, graphics_folder
from common import PostUnit, AlertPopup, redirection, searchlog


Builder.load_file(GUI_folder + '/post_screen_GUI.kv')

# 프로필로 가는 버튼 레이아웃 클래스
class ButtonLayout(ButtonBehavior, BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

# 게시글 스크린 클래스
class PostScreen(Screen):
    bg_path = graphics_folder + '/post_background.jpg'
    redirection = None
    category = 'all'
    order = 'id'
    # 게시글 스크린으로 들어가기 직전의 행동이다
    def on_pre_enter(self, *args):
        userinfo = usersdbinterface.get_userinfo()
        if type(userinfo) == ResponseException:
            AlertPopup('Adjust error!', str(userinfo)).open()
            self.goto_login_screen()
            return
        nickname = userinfo.get('nickname')
        self.ids.welcome_message.text = 'Welcome, ' + nickname + '!'
        # 리다이렉션이 있으면 리다이렉트 하고 없으면 모든 부모가 ''인 것을 보여준다
        self.updateposts(redirection.get_redirection())
        redirection.set_redirection(None)
    # 부모가 되는 게시글과 그것의 자식 게시글들을 소환한다
    def updateposts(self, id_prefix=None, where='', order=''):
        # 초기화 과정
        if self.ids.body.children != []:
            self.ids.body.clear_widgets()
        # id_prefix에 값이 전달되지 않으면 기존값을 유지하고, 값이 전달되면 값을 바꾼다. 
        if id_prefix == None:
            id_prefix = postsdbinterface.get_id_prefix()
        else:
            postsdbinterface.put_id_prefix(id_prefix)
        # parent가 ''이면 공지사항 게시글을 맨 위에 추가한다
        if id_prefix == '' and where == '' and order == '':
            self.ids.body.add_widget(PostUnit(
                '', 
                'NotTwitter', 
                '2000-00-00', 
                "Welcome to this app!\n" + 
                "This is copycat of Twitter(current day X),\n" +
                "but this app cannot edit or delete your post,\n" +
                "cause it is no use crying over spilt milk.\n" +
                "Post carefully!",
                lambda : None))
        # 부모와 자식 게시들을의 id를 소환해, 이들을 통해 화면에 게시글들을 표시한다
        postlist = postsdbinterface.get_postlist(where, order)
        if type(postlist) == ResponseException:
            AlertPopup('Adjust error!', str(postlist)).open()
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
            action = lambda id=id : self.updateposts(id)
            self.ids.body.add_widget(PostUnit(id, writer, writedate, content, action))
        # 로그에 값을 저장한다
        if id_prefix != '':
            searchlog.add(id_prefix)
    # 스피너의 값을 저장한다
    def spinner_select(self, spinner):
        match spinner:
            case self.ids.category:
                self.category = spinner.text
            case self.ids.order:
                self.order = spinner.text
    # 게시글을 검색한다
    def searchposts(self, *args):
        searchword = self.ids.search_text.text
        match self.ids.category.text:
            case 'All':
                where = None
            case 'Content':
                where = 'posts.content LIKE "%{}%"'.format(searchword)
            case 'Writer':
                where = 'user.username LIKE "%{}%"'.format(searchword)
            case _:
                return
        match self.ids.order.text:
            case 'Default order':
                order = 'id'
            case 'Content order':
                order = 'content'
            case 'Writer order':
                order = 'writer'
            case _:
                return
        self.updateposts(where=where, order=order)
    # 이전에 방문한 게시글 및 그의 자식들을 불러온다
    def go_prev(self, *args):
        log = searchlog.prev()
        if log == None:
            return
        else:
            self.updateposts(log)
    # 이후에 방문한 게시글 및 그의 자식들을 불러온다
    def go_next(self, *args):
        log = searchlog.next()
        if log == None:
            return
        else:
            self.updateposts(log)
    # 로그인 스크린으로 들어간다
    def goto_login_screen(self):
        self.manager.current = 'Login Screen'
    # 게시글 작성 스크린으로 들어간다
    def goto_edit_screen(self):
        self.manager.current = 'Edit Screen'
    # 프로필 스크린으로 들어간다
    def goto_profile_screen(self, usernum=None):
        if usernum == None:
            usernum = usersdbinterface.get_header().get('usernum')
        profilewhom.set_usernum(usernum)
        self.manager.current = 'Profile Screen'
    # 환경설정 스크린으로 들어간다
    def goto_setting_screen(self):
        self.manager.current = 'Setting Screen'
postscreen = PostScreen(name='Post Screen')
