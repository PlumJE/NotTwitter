from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from time import sleep

from db_interface import userdetaildbinterface, usersdbinterface
from folder_paths import GUI_folder, graphics_folder

Builder.load_file(GUI_folder + '/profile_screen_GUI.kv')

class ProfileScreen(Screen):
    _register_mode = False
    _edit_mode = False
    bg_path = graphics_folder + '/post_background.jpg'
    def on_pre_enter(self, *args):
        if self._register_mode == True:
            self.ids.loginlayout.remove_widget(self.ids.firstloginlayout)
            self.ids.loginlayout.remove_widget(self.ids.lastloginlayout)

            self.change_profile(*args)
        else:
            self.ids.loginlayout.add_widget(self.ids.firstloginlayout)
            self.ids.loginlayout.add_widget(self.ids.lastloginlayout)

            userinfo = usersdbinterface.get_userinfo()
            self.ids.nickname.text = userinfo.get('nickname')
            self.ids.firstname.text = userinfo.get('firstname')
            self.ids.lastname.text = userinfo.get('lastname')
            self.ids.firstlogin.text = userinfo.get('firstlogin')
            self.ids.lastlogin.text = userinfo.get('lastlogin')

            userdetail = userdetaildbinterface.get_userinfo()
            self.ids.birth.text = userdetail.get('birth')
            self.ids.phone.text = userdetail.get('phone')
            self.ids.families.text = userdetail.get('families')
            self.ids.nation.text = userdetail.get('nation')
            self.ids.legion.text = userdetail.get('legion')
            self.ids.job.text = userdetail.get('job')
            self.ids.jobaddr.text = userdetail.get('jobaddr')
    def activate_register_mode(self):
        self._register_mode = True
    def hide_widget(self, widget):
        widget.height = 0
        widget.size_hint_y = None
        widget.opacity = 0
        widget.disabled = True
    def show_widget(self, widget):
        widget.height = self.ids.nicknamelayout.height
        widget.size_hint_y = self.ids.nicknamelayout.size_hint_y
        widget.opacity = 1
        widget.disabled = False
    def change_profile(self, *args):
        if self._edit_mode == True:
            return
        
        self._edit_mode = True
        self.ids.changeSaveBtn.text = 'Save'
        self.ids.changeSaveBtn.on_release = self.save_profile

        self.ids.nickname.readonly = False
        self.ids.firstname.readonly = False
        self.ids.lastname.readonly = False
        self.ids.birth.readonly = False
        self.ids.phone.readonly = False
        self.ids.families.readonly = False
        self.ids.nation.readonly = False
        self.ids.legion.readonly = False
        self.ids.job.readonly = False
        self.ids.jobaddr.readonly = False
    def save_profile(self, *args):
        if self._edit_mode == False:
            return
        
        self._edit_mode = False
        birth = self.ids.birth.text
        phone = self.ids.phone.text
        families = self.ids.families.text
        nation = self.ids.nation.text
        legion = self.ids.legion.text
        job = self.ids.job.text
        jobaddr = self.ids.jobaddr.text
        userdetaildbinterface.put_userinfo(birth, phone, families, nation, legion, job, jobaddr)

        self.ids.changeSaveBtn.text = 'Change'
        self.ids.changeSaveBtn.on_release = self.change_profile

        self.ids.nickname.readonly = True
        self.ids.firstname.readonly = True
        self.ids.lastname.readonly = True
        self.ids.birth.readonly = True
        self.ids.phone.readonly = True
        self.ids.families.readonly = True
        self.ids.nation.readonly = True
        self.ids.legion.readonly = True
        self.ids.job.readonly = True
        self.ids.jobaddr.readonly = True

        sleep(0.5)
    def goto_post_screen(self):
        self.register_mode = False
        self.manager.current = 'Post Screen'
profilescreen = ProfileScreen(name='Profile Screen')