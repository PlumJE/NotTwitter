from logging import Logger, FileHandler, DEBUG
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior

from folder_paths import GUI_folder


Builder.load_file(GUI_folder + '/common_GUI.kv')

# 게시글 유닛 클래스
class PostUnit(ButtonBehavior, BoxLayout):
    # 게시글에 게시글id, 작성자id, 작성날짜, 내용, 클릭시 행동을 입력해 게시글 유닛을 생성한다
    def __init__(self, id, writer, writedate, content, action, profileimg=None, postimg=None, **kwargs):
        super(PostUnit, self).__init__(**kwargs)

        self._id = id
        self.ids.writer.text = 'Writer : ' + writer if writer is not None else ''
        self.ids.writedate.text = 'Write date : ' + writedate if writedate is not None else ''
        self.ids.content.text = content
        self.on_release = action
        if profileimg:
            self.ids.profile_layout.add_widget(profileimg)
        if postimg:
            self.ids.postimg_layout.add_widget(postimg)
        

# 클릭 가능한 사진 클래스
class ClickableImg(ButtonBehavior, AsyncImage):
    def __init__(self, path, action=None, **kwargs):
        super(ClickableImg, self).__init__(**kwargs)
        if path is not None:
            self.source = 'http://127.0.0.1:8000/media/' + path

        if action:
            self.on_release = action
    def change_image(self, path):
        if path is not None:
            self.source = 'http://127.0.0.1:8000/media/' + path

# Alert 메시지를 보내는 팝업창
class AlertPopup(Popup):
    def __init__(self, title, content, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.content = Label(text=content)
        self.size_hint=(1, 0.2)
        self.auto_dismiss=True

# Yes랑 No중에 선택하는 팝업창
class SelectPopup(Popup):
    def __init__(self, title, content, yesText, noText, yesFunc=None, noFunc=None, **kwargs):
        super().__init__(**kwargs)

        self.title = title
        self.ids.content.text = content

        self.ids.yesBtn.text = yesText
        self.yesFunc = yesFunc

        self.ids.noBtn.text = noText
        self.noFunc = noFunc
    def select(self, yes):
        if yes and self.yesFunc:
            self.yesFunc()
        elif not yes and self.noFunc:
            self.noFunc()
        self.dismiss();

# 입력값을 입력하는 팝업창
class InsertPopup(Popup):
    def __init__(self, title, content, callback, is_secret=False, **kwargs):
        super().__init__(**kwargs)

        self.title = title
        self.ids.content.text = content

        self.callback = callback
        self.ids.text_input.password = is_secret
    def insert(self):
        if self.callback:
            self.callback(self.ids.text_input.text)
            self.dismiss()

# 파일 선택 팝업창
class FileChooserPopup(Popup):
    def __init__(self, title, callback, **kwargs):
        super().__init__(**kwargs)

        self.title = title
        self.callback = callback
    def load_file(self):
        if self.callback and self.ids.filechooser.selection:
            self.callback(self.ids.filechooser.selection)
            self.dismiss()

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

# 리다이렉션 클래스
class Redirection:
    __redirection = None
    def set_redirection(self, redirection):
        self.__redirection = redirection
    def get_redirection(self):
        return self.__redirection
redirection = Redirection()

# debug_mode == True일 때만 작동하는 로거 클래스
class MyLogger(Logger):
    def __init__(self, onoff, name=None, level=DEBUG, save_path='app_log.log'):
        super(MyLogger, self).__init__(name, level)
        self.__onoff = onoff
        if onoff == True:
            self.addHandler(FileHandler(save_path))
    def debug(self, msg, *args, exc_info=None, stack_info=False, stacklevel=1, extra=None):
        if self.__onoff == True:
            return super().debug(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)
    def info(self, msg, *args, exc_info=None, stack_info=False, stacklevel=1, extra=None):
        if self.__onoff == True:
            return super().info(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)
    def warning(self, msg, *args, exc_info=None, stack_info=False, stacklevel=1, extra=None):
        if self.__onoff == True:
            return super().warning(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)
    def error(self, msg, *args, exc_info=None, stack_info=False, stacklevel=1, extra=None):
        if self.__onoff == True:
            return super().error(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)
    def critical(self, msg, *args, exc_info=None, stack_info=False, stacklevel=1, extra=None):
        if self.__onoff == True:
            return super().critical(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)
logger = MyLogger(True)
