from requests import post, get, put, delete
from requests.exceptions import *

from common import AlertPopup

# 응답 코드를 저장한 예외 클래스
class ResponseException(RequestException):
    def __init__(self, code, message):
        self.code = code
        self.message = message
    def __str__(self):
        return '{} : {}'.format(self.code, self.message)

# 서버와의 인터페이스 베이스 클래스
class DBInterface:
    _url = 'http://127.0.0.1:8000/'
    # http 통신을 실행하는 함수. json()결과물이나 ResponseException()을 리턴만 하고, 예외를 발생시키지 않는다.
    def __execute(self, method, url, headers, data, **kwargs):
        try:
            response = method(url, headers=headers, data=data, **kwargs)
            response.raise_for_status()
            return response.json()
        except ConnectionError:
            return ResponseException(503, 'Failed to connect to the server.')
        except InvalidURL:
            return ResponseException(400, 'URL is invalid.')
        except Timeout:
            return ResponseException(408, 'The request timed out.')
        except SSLError:
            return ResponseException(495, 'SSL certificate error.')
        except HTTPError as e:
            return ResponseException(e.response.status_code, e.response.json().get('error'))
        except Exception as e:
            return ResponseException(499, 'Internal client error.')
    def _post(self, url, headers={}, data={}, **kwargs):
        return self.__execute(post, url, headers, data, **kwargs)
    def _get(self, url, headers={}, data={}, **kwargs):
        return self.__execute(get, url, headers, data, **kwargs)
    def _put(self, url, headers={}, data={}, **kwargs):
        return self.__execute(put, url, headers, data, **kwargs)
    def _delete(self, url, headers={}, data={}, **kwargs):
        return self.__execute(delete, url, headers, data, **kwargs)

# 유저 관리 인터페이스 클래스
class UsersDBInterface(DBInterface):
    def __init__(self):
        super(UsersDBInterface, self).__init__()
        self.__token = ''
        self._url += 'users/'
        self.usernum = 0
    # http 헤더를 생성
    def get_header(self):
        return {
            'Authorization': 'Token ' + self.__token,
            'usernum': str(self.usernum)
        }
    # 로그인 성공시 유저번호, 처음보는 계정이면 0, 실패시 None을 리턴
    def login(self, nickname, mailaddr, password):
        url = self._url + 'loginout/'
        data = {
            'nickname': nickname,
            'mailaddr': mailaddr,
            'password': password
        }

        response = self._post(url, data=data)
        if type(response) == ResponseException:
            AlertPopup('Login Error!', str(response)).open()
            return
        
        self.__token = response.get('token')
        self.usernum = response.get('usernum')
        return self.usernum
    # 로그아웃 성공시 True, 실패시 False를 리턴
    def logout(self):
        url = self._url + 'loginout/'
        headers = self.get_header()

        response = self._delete(url, headers=headers)
        if type(response) == ResponseException:
            AlertPopup('Logout Error!', str(response)).open()
            return False

        self.__token = ''
        self.usernum = 0
        return True
    # 성공시 True, 실패시 False를 리턴
    def post_userinfo(self, nickname, mailaddr, password):
        url = self._url + 'userinfo/'
        data = {
            'nickname': nickname,
            'mailaddr': mailaddr,
            'password': password
        }

        response = self._post(url, data=data)
        if type(response) == ResponseException:
            AlertPopup('User Error!', str(response)).open()
            return False
        
        return True
    # 성공시 유저정보, 실패시 None을 리턴
    def get_userinfo(self, usernum=None):
        url = self._url + 'userinfo/'
        headers = self.get_header()
        data = {
            'usernum': usernum if usernum else self.usernum
        }

        response = self._get(url, headers=headers, data=data)
        if type(response) == ResponseException:
            AlertPopup('User Error!', str(response)).open()
            return
        
        return response
    # 성공시 유저정보, 실패시 None을 리턴
    def put_userinfo(self, nickname, mailaddr, firstname, lastname):
        url = self._url + 'userinfo/'
        headers = self.get_header()
        data = {
            'nickname': nickname,
            'mailaddr': mailaddr,
            'firstname': firstname,
            'lastname': lastname
        }

        response = self._put(url, headers=headers, data=data)
        if type(response) == ResponseException:
            AlertPopup('User Error!', str(response)).open()
            return
        
        return response
    # 성공시 True, 실패시 False를 리턴
    def delete_userinfo(self):
        url = self._url + 'userinfo/'
        headers = self.get_header()
        data = {}

        response = self._delete(url, headers=headers, data=data)
        if type(response) == ResponseException:
            AlertPopup('User Error!', str(response)).open()
            return False
        
        self.__token = ''
        self.usernum = 0
        return True
usersdbinterface = UsersDBInterface()

# 유저 상세정보 관리 인터페이스 클래스
class UserDetailsDBInterface(DBInterface):
    def __init__(self):
        super(UserDetailsDBInterface, self).__init__()
        self._url += 'users/'
    # 성공시 True, 실패시 False를 리턴
    def post_userdetail(self, usernum):
        url = self._url + 'userdetail/'
        headers = usersdbinterface.get_header()
        data = {
            'usernum': usernum
        }

        response = self._post(url, headers=headers, data=data)
        if type(response) == ResponseException:
            AlertPopup('User Detail Error!', str(response)).open()
            return False
        
        return True
    # 성공시 유저상세정보, 실패시 None을 리턴
    def get_userdetail(self, usernum=None):
        url = self._url + 'userdetail/'
        headers = usersdbinterface.get_header()
        data = {
            'usernum': usernum if usernum else int(headers.get('usernum'))
        }

        response = self._get(url, headers=headers, data=data)
        if type(response) == ResponseException:
            AlertPopup('User Detail Error!', str(response)).open()
            return
        
        return response
    # 성공시 유저상세정보, 실패시 None을 리턴
    def put_userdetail(self, birth, phone, families, nation, legion, job, jobaddr):
        url = self._url + 'userdetail/'
        headers = usersdbinterface.get_header()
        data = {
            'birth': birth,
            'phone': phone,
            'families': families,
            'nation': nation,
            'legion': legion,
            'job': job,
            'jobaddr': jobaddr
        }

        response = self._put(url, headers=headers, data=data)
        if type(response) == ResponseException:
            AlertPopup('User Detail Error!', str(response)).open()
            return
        
        return response
    # 성공시 True, 실패시 False을 리턴
    def delete_userdetail(self):
        url = self._url + 'userdetail/'
        headers = usersdbinterface.get_header()
        data = {}

        response = self._put(url, headers=headers, data=data)
        if type(response) == ResponseException:
            AlertPopup('User Detail Error!', str(response)).open()
            return False
        
        return True
    # 성공시 True, 실패시 False를 리턴
    def upload_profile(self, image_path):
        url = self._url + 'profileimg/'
        headers = usersdbinterface.get_header()
        data = {
            'usernum': int(headers.get('usernum'))
        }

        with open(image_path, 'rb') as image:
            files = {'profileimg': image}
            
            response = self._put(url, headers=headers, data=data, files=files)
            if type(response) == ResponseException:
                AlertPopup('Profile save Error!', str(response)).open()
                return False
        return True
    # 성공시 이미지url, 실패시 'images/profiles/default.jpeg'을 리턴
    def download_profile(self, usernum=None):
        url = self._url + 'profileimg/'
        headers = usersdbinterface.get_header()
        data = {
            'usernum': usernum if usernum else int(headers.get('usernum'))
        }
        
        response = self._get(url, headers=headers, data=data)
        if type(response) == ResponseException:
            AlertPopup('Profile load Error!', str(response)).open()
            return

        profile_name = response.get('profile_name')
        return profile_name
userdetaildbinterface = UserDetailsDBInterface()

# 포스트 관리 인터페이스 클래스
class PostsDBInterface(DBInterface):
    def __init__(self):
        super(PostsDBInterface, self).__init__()
        self._url += 'posts/'
        self.id_prefix = ''
    # 성공시 포스트 번호 리스트, 실패시 None을 리턴
    def get_postlist(self, where='', order=''):
        url = self._url + 'postlist/'
        headers = usersdbinterface.get_header()
        data = {
            'id_prefix': self.id_prefix,
            'where': where,
            'order': order
        }

        response = self._get(url, headers=headers, data=data)
        if type(response) == ResponseException and response.code != 404:
            AlertPopup('Posting Error!', str(response)).open()
            return

        return response.get('id_list')
    # 성공시 포스트 정보, 실패시 None을 리턴
    def get_post(self, id):
        url = self._url + 'post/'
        headers = usersdbinterface.get_header()
        data = {
            'id': id
        }

        response = self._get(url, headers=headers, data=data)
        if type(response) == ResponseException and response.status_code != 404:
            AlertPopup('Posting Error!', str(response)).open()
            return
        
        return response
    # 성공시 포스트 번호, 실패시 None을 리턴
    def post_post(self, writedate, content):
        url = self._url + 'post/'
        headers = usersdbinterface.get_header()
        data = {
            'id_prefix': self.id_prefix,
            'writer': headers.get('usernum'),
            'writedate': writedate,
            'content': content
        }

        response = self._post(url, headers=headers, data=data)
        if type(response) == ResponseException:
            AlertPopup('Posting Error!', str(response)).open()
            return
        
        return response.get('id')
        # 성공시 True, 실패시 False를 리턴
    # 성공시 True, 실패시 False를 리턴
    def upload_postimg(self, id, image_path):
        url = self._url + 'postimg/'
        headers = usersdbinterface.get_header()
        data = {
            'id': id
        }

        with open(image_path, 'rb') as image:
            files = {'postimg': image}
            
            response = self._put(url, headers=headers, data=data, files=files)
            if type(response) == ResponseException:
                AlertPopup('Postimg save Error!', str(response)).open()
                return False
        return True
    # 성공시 이미지url, 실패시 None을 리턴
    def download_postimg(self, id):
        url = self._url + 'postimg/'
        headers = usersdbinterface.get_header()
        data = {
            'id': id
        }
        print('hello')
        response = self._get(url, headers=headers, data=data)
        if type(response) == ResponseException:
            AlertPopup('Postimg load Error!', str(response)).open()
            return
        print('hi')
        postimg_name = response.get('postimg_name')
        return postimg_name
    # 현재 id_prefix를 읽음
    def get_id_prefix(self):
        return self.id_prefix
    # 현재 id_prefix를 새로 씀
    def put_id_prefix(self, id_prefix):
        self.id_prefix = id_prefix
postsdbinterface = PostsDBInterface()
