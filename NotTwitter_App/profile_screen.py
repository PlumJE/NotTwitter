from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from custom_popup import ErrorPopup, InsertPopup
from db_interface import ResponseException, userdetaildbinterface, usersdbinterface
from folder_paths import GUI_folder, graphics_folder

Builder.load_file(GUI_folder + '/profile_screen_GUI.kv')

class ProfileScreen(Screen):
    register_mode = False
    write_mode = False
    bg_path = graphics_folder + '/post_background.jpg'
    def on_pre_enter(self, *args):
        if self.register_mode:
            self.go_write_mode()
            self.hide_widget(self.ids.nicknamelayout)
            self.hide_widget(self.ids.firstloginlayout)
            self.hide_widget(self.ids.lastloginlayout)
        else:
            self.load_profile()
            self.show_widget(self.ids.nicknamelayout)
            self.show_widget(self.ids.firstloginlayout)
            self.show_widget(self.ids.lastloginlayout)
    def on_leave(self, *args):
        self.register_mode = False
        self.password = ''
        self.clean_profile()
        self.go_read_mode()
    def change_save_button(self, *args):
        if self.register_mode:
            self.save_profile()
        else:
            if self.write_mode:
                self.go_read_mode()
                self.save_profile()
            else:
                self.go_write_mode()
    def exit_button(self, *args):
        if self.register_mode:
            self.goto_login_screen()
        else:
            self.goto_post_screen()
    def start_register_mode(self, nickname, password):
        self.ids.nickname.text = nickname
        self.password = password
        self.register_mode = True
        self.manager.current = 'Profile Screen'
    def hide_widget(self, widget):
        widget.size_hint = (None, None)
        widget.size = (0, 0)
        widget.opacity = 0
        widget.disabled = True
    def show_widget(self, widget):
        widget.size_hint = self.ids.mailaddrlayout.size_hint
        widget.size = self.ids.mailaddrlayout.size
        widget.opacity = 1
        widget.disabled = False
    def go_read_mode(self):
        if not self.write_mode:
            return
        self.write_mode = False

        self.ids.changeSaveBtn.text = 'Change'
        self.ids.nickname.readonly = True
        self.ids.mailaddr.readonly = True
        self.ids.firstname.readonly = True
        self.ids.lastname.readonly = True
        self.ids.birth.readonly = True
        self.ids.phone.readonly = True
        self.ids.families.readonly = True
        self.ids.nation.readonly = True
        self.ids.legion.readonly = True
        self.ids.job.readonly = True
        self.ids.jobaddr.readonly = True
    def go_write_mode(self):
        if self.write_mode:
            return
        self.write_mode = True

        self.ids.changeSaveBtn.text = 'Save'
        self.ids.nickname.readonly = False
        self.ids.mailaddr.readonly = False
        self.ids.firstname.readonly = False
        self.ids.lastname.readonly = False
        self.ids.birth.readonly = False
        self.ids.phone.readonly = False
        self.ids.families.readonly = False
        self.ids.nation.readonly = False
        self.ids.legion.readonly = False
        self.ids.job.readonly = False
        self.ids.jobaddr.readonly = False
    def load_profile(self):
        userinfo = usersdbinterface.get_userinfo()
        if type(userinfo) == ResponseException:
            ErrorPopup('Load Error!', str(userinfo)).open()
            self.goto_post_screen()
            return
        
        self.ids.nickname.text = userinfo.get('nickname')
        self.ids.mailaddr.text = userinfo.get('mailaddr')
        self.ids.firstname.text = userinfo.get('firstname')
        self.ids.lastname.text = userinfo.get('lastname')
        self.ids.firstlogin.text = userinfo.get('firstlogin')
        self.ids.lastlogin.text = userinfo.get('lastlogin')

        userdetail = userdetaildbinterface.get_userdetail()
        if type(userdetail) == ResponseException:
            ErrorPopup('Load Error!', str(userdetail)).open()
            # self.goto_post_screen()
            return
        
        self.ids.birth.text = userdetail.get('birth')
        self.ids.phone.text = userdetail.get('phone')
        self.ids.families.text = userdetail.get('families')
        self.ids.nation.text = userdetail.get('nation')
        self.ids.legion.text = userdetail.get('legion')
        self.ids.job.text = userdetail.get('job')
        self.ids.jobaddr.text = userdetail.get('jobaddr') 
    def save_profile(self):
        nickname = self.ids.nickname.text
        mailaddr = self.ids.mailaddr.text
        firstname = self.ids.firstname.text
        lastname = self.ids.lastname.text
        
        birth = self.ids.birth.text
        phone = self.ids.phone.text
        families = self.ids.families.text
        nation = self.ids.nation.text
        legion = self.ids.legion.text
        job = self.ids.job.text
        jobaddr = self.ids.jobaddr.text
        
        if self.register_mode:
            result = usersdbinterface.post_userinfo(nickname, self.password, mailaddr, firstname, lastname)
            if type(result) == ResponseException:
                ErrorPopup('Save Error!', str(result)).open()
                return
            
            usernum = result.get('usernum')

            result = userdetaildbinterface.post_userdetail(usernum, birth, phone, families, nation, legion, job, jobaddr)
            if type(result) == ResponseException:
                ErrorPopup('Save Error!', str(result)).open()
                return
            
            ErrorPopup('Register Succeeded!!', 'Please login again in the login screen').open()
            self.goto_login_screen()
        else:
            result = usersdbinterface.put_userinfo(nickname, mailaddr, firstname, lastname)
            if type(result) == ResponseException:
                ErrorPopup('Save Error!', str(result)).open()
                return

            result = userdetaildbinterface.put_userdetail(birth, phone, families, nation, legion, job, jobaddr)
            if type(result) == ResponseException:
                ErrorPopup('Save Error!', str(result)).open()
                return

            ErrorPopup('Profile Save Complete!').open()
    def clean_profile(self):
        self.ids.nickname.text = ''
        self.ids.mailaddr.text = ''
        self.ids.firstname.text = ''
        self.ids.lastname.text = ''
        self.ids.firstlogin.text = ''
        self.ids.lastlogin.text = ''

        self.ids.birth.text = ''
        self.ids.phone.text = ''
        self.ids.families.text = ''
        self.ids.nation.text = ''
        self.ids.legion.text = ''
        self.ids.job.text = ''
        self.ids.jobaddr.text = ''
    def goto_login_screen(self):
        self.manager.current = 'Login Screen'
    def goto_post_screen(self):
        self.manager.current = 'Post Screen'
profilescreen = ProfileScreen(name='Profile Screen')