from datetime import datetime
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen

from db_interface import ResponseException, usersdbinterface, postsdbinterface
from common import AlertPopup
from folder_paths import GUI_folder, graphics_folder


Builder.load_file(GUI_folder + '/edit_screen_GUI.kv')

# 게시글 작성 스크린 클래스
class EditScreen(Screen):
    bg_path = graphics_folder + '/post_background.jpg'
    writer = ''
    writedate = ''
    # 게시글 작성 스크린으로 들어가기 직전의 행동이다. 작성자id, 작성자 닉네임, 현재 날짜를 얻어내, 작성자 닉네임, 현재 날짜를 스크린에 띄운다
    def on_pre_enter(self, *args):
        userinfo = usersdbinterface.get_userinfo()
        if type(userinfo) == ResponseException:
            AlertPopup('Adjust error!', str(userinfo)).open()
            self.goto_post_screen()
            return
        self.writer = userinfo.get('nickname')
        self.writedate = str(datetime.now().date())
        self.ids.writer.text = 'Writer : ' + self.writer
        self.ids.writedate.text = 'Write date : ' + self.writedate
        self.ids.content.text = ''
    # 게시글을 데이터베이스에 올린다
    def adjust(self, *args):
        content = self.ids.content.text
        if content == '' or content.isspace():
            return
        result = postsdbinterface.post_post(self.writedate, content)
        if type(result) == ResponseException:
            AlertPopup('Adjust error!', str(result)).open()
            return
        editscreen.goto_post_screen()
    # 게시글 작성을 포기한다
    def discard(self, *args):
        editscreen.goto_post_screen()
    # 게시글 스크린으로 들어간다
    def goto_post_screen(self):
        self.manager.current = 'Post Screen'
editscreen = EditScreen(name='Edit Screen')