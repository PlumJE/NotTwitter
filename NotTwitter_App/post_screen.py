from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.behaviors import ButtonBehavior

from db_interface import usersdbinterface, postsdbinterface
from folder_paths import GUI_folder, graphics_folder
from debug import logger


Builder.load_file(GUI_folder + '/post_screen_GUI.kv')

# 지금까지 찾아다닌 게시글들의 id들의 이력들을 저장하는 클래스
class SearchLog:
    logs = ['']
    ptr = 0
    # 스택에 추가한다
    def add(self, log):
        if self.ptr < len(self.logs) - 1:
            del self.logs[self.ptr + 1:]
        self.logs.append(log)
        self.ptr += 1
        logger.debug("Search log is : " + str(self.logs))
    # 스택의 이전 요소로 간다
    def prev(self):
        if self.ptr > 0:
            self.ptr -= 1
            return self.logs[self.ptr]
        else:
            return
    # 스택의 다음 요소로 간다
    def next(self):
        if self.ptr < len(self.logs) - 1:
            self.ptr += 1
            return self.logs[self.ptr]
        else:
            return
searchlog = SearchLog()

# 게시글 유닛 클래스
class PostUnit(ButtonBehavior, BoxLayout):
    # 게시글에 게시글id, 작성자id, 작성날짜, 내용을 입력해 게시글 유닛을 생성한다
    def __init__(self, id, writer, writedate, content, **kwargs):
        super(PostUnit, self).__init__(**kwargs)
        self._id = id
        self.ids.writer.text += writer
        self.ids.writedate.text += writedate
        self.ids.content.text = content
    # 게시글을 클릭하면 해당 게시글과 그것의 자식 게시글들을 소환한다. 다만 공지사항을 클릭하면 작동하지 않는다
    def updateposts(self, *args):
        # 공지사항 게시글 유닛인 경우...
        if self._id != '':
            searchlog.add(self._id)
            postscreen.updateposts(self._id)

# 게시글 스크린 클래스
class PostScreen(Screen):
    bg_path = graphics_folder + '/post_background.jpg'
    # 게시글 스크린으로 들어가기 직전의 행동이다
    def on_pre_enter(self, *args):
        nickname = usersdbinterface.get_nickname()
        if type(nickname) == Popup:
            nickname.open()
            self.goto_login_screen()
            return
        self.ids.welcome_message.text = 'Welcome, ' + nickname + '!'
        self.updateposts()
    # 부모가 되는 게시글과 그것의 자식 게시글들을 소환한다
    def updateposts(self, id_prefix=None):
        # 초기화 과정
        if self.ids.body.children != []:
            self.ids.body.clear_widgets()
        # id_prefix를 변경하거나 불러온다
        if id_prefix != None:
            postsdbinterface.put_id_prefix(id_prefix)
        id_prefix = postsdbinterface.get_id_prefix()
        # parent가 ''이면 공지사항 게시글을 맨 위에 추가한다
        if (id_prefix == ''):
            self.ids.body.add_widget(PostUnit('', 'NotTwitter', '2000-00-00', 
"""Welcome to this app!
This is copycat of Twitter(current day X),
but this app cannot edit or delete your post,
cause it is no use crying over spilt milk.
Post carefully!"""))
        # 부모와 자식 게시들을의 id를 소환해, 이들을 통해 화면에 게시글들을 표시한다
        postlist = postsdbinterface.get_postlist()
        if type(postlist) == Popup:
            postlist.open()
            self.goto_login_screen()
            return
        for post in postlist:
            result = postsdbinterface.get_post(post)
            if type(result) == Popup:
                result.open()
                self.goto_login_screen()
                return
            id = result.get('id')
            writer = result.get('writer')
            print('writer is', writer)
            writer = usersdbinterface.get_nickname(writer)
            if type(writer) == Popup:
                writer.open()
                self.goto_login_screen()
                return
            writedate = result.get('writedate')
            content = result.get('content')
            self.ids.body.add_widget(PostUnit(id, writer, writedate, content))
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
    # 환경설정 스크린으로 들어간다
    def goto_setting_screen(self):
        self.manager.current = 'Setting Screen'
postscreen = PostScreen(name='Post Screen')
