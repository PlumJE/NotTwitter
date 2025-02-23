from datetime import datetime
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen

from db_interface import usersdbinterface, postsdbinterface
from folder_paths import GUI_folder, graphics_folder
from common import ClickableImg, FileChooserPopup


Builder.load_file(GUI_folder + '/edit_screen_GUI.kv')

# 게시글 작성 스크린 클래스
class EditScreen(Screen):
    bg_path = graphics_folder + '/post_background.jpg'
    writer = ''
    writedate = ''
    postimg_path = ''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filechooser = FileChooserPopup('Select Image', self.bring_img)
        self.postimg = ClickableImg(
            '/images/postimgs/add_image.png',
            lambda self=self : self.filechooser.open()
        )
        self.ids.body.add_widget(self.postimg)
    # 게시글 작성 스크린으로 들어가기 직전의 행동이다. 작성자id, 작성자 닉네임, 현재 날짜를 얻어내, 작성자 닉네임, 현재 날짜를 스크린에 띄운다
    def on_pre_enter(self, *args):
        userinfo = usersdbinterface.get_userinfo()
        if userinfo is None:
            self.goto_post_screen()
            return
        
        self.writer = userinfo.get('nickname')
        self.writedate = str(datetime.now().date())
        self.ids.writer.text = 'Writer : ' + self.writer
        self.ids.writedate.text = 'Write date : ' + self.writedate
        self.ids.content.text = ''
        self.postimg.change_image('/images/postimgs/add_image.png')
    # 이미지를 불러온다
    def bring_img(self, paths):
        self.postimg.source = paths[0]
        self.postimg_path = paths[0]
    # 게시글을 데이터베이스에 올린다
    def adjust(self, *args):
        content = self.ids.content.text
        postimg_path = self.postimg_path
        if (not content or content.isspace()) and (not postimg_path or postimg_path.isspace()):
            return

        postnum = postsdbinterface.post_post(self.writedate, content)
        if postnum is None:
            return
        
        if postimg_path:
            result = postsdbinterface.upload_postimg(postnum, postimg_path)
            if not result:
                return
        
        self.postimg.change_image('/images/postimgs/add_image.png')
        self.postimg_path = ''

        editscreen.goto_post_screen()
    # 게시글 작성을 포기한다
    def discard(self, *args):
        editscreen.goto_post_screen()
    # 게시글 스크린으로 들어간다
    def goto_post_screen(self):
        self.manager.current = 'Post Screen'
editscreen = EditScreen(name='Edit Screen')