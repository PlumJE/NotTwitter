from requests import post, get, put, delete, patch
from requests.exceptions import *


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
    # http 통신을 실행하는 함수. json()결과물이나 REsponseException()을 리턴만 하고, 예외를 발생시키지 않는다.
    def __execute(self, method, url, headers, data):
        try:
            response = method(url, headers=headers, data=data)
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
    def _post(self, url, headers={}, data={}):
        return self.__execute(post, url, headers, data)
    def _get(self, url, headers={}, data={}):
        return self.__execute(get, url, headers, data)
    def _put(self, url, headers={}, data={}):
        return self.__execute(put, url, headers, data)
    def _delete(self, url, headers={}, data={}):
        return self.__execute(delete, url, headers, data)

# 유저 관리 인터페이스 클래스
class UsersDBInterface(DBInterface):
    def __init__(self):
        super(UsersDBInterface, self).__init__()
        self._url += 'users/'
        self._token = ''
        self._usernum = 0
    # http 헤더를 생성
    def get_header(self):
        return {
            'Authorization': 'Token ' + self._token,
            'usernum': str(self._usernum)
        }
    # 처음오면 false, 온 적이 있으면 true, 실패시 ResponseException을 리턴
    def login(self, nickname, password):
        url = self._url + 'loginout/'
        data = {
            'nickname': nickname,
            'password': password
        }

        response = self._post(url, data=data)

        if type(response) == ResponseException:
            return response
        
        self._token = response.get('token')
        self._usernum = response.get('usernum')
    # 성공시 None, 실패시 ResponseException을 리턴
    def logout(self):
        url = self._url + 'loginout/'
        headers = self.get_header()

        response = self._delete(url, headers=headers)

        if type(response) == ResponseException:
            return response

        self._token = ''
        self._usernum = 0
    # 로그인 상태인지 아님 로그아웃 상태인지 판별
    def is_login(self):
        if self._usernum and self._token:
            return True
        else:
            return False
    # 성공시 유저번호, 실패시 ResponseException을 리턴
    def post_userinfo(self, nickname, password, mailaddr, firstname, lastname):
        url = self._url + 'userinfo/'
        data = {
            'nickname': nickname,
            'password': password,
            'mailaddr': mailaddr,
            'firstname': firstname,
            'lastname': lastname
        }

        response = self._post(url, data=data)

        if type(response) == ResponseException:
            return response
        
        return response
    # 성공시 유저정보, 실패시 ResponseException을 리턴
    def get_userinfo(self, usernum=None):
        url = self._url + 'userinfo/'
        headers = self.get_header()
        data = {
            'usernum': usernum if usernum else self._usernum
        }

        response = self._get(url, headers=headers, data=data)

        if type(response) == ResponseException:
            return response
        
        return response
    # 성공시 None, 실패시 ResponseException을 리턴
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
            return response
    # 성공시 None, 실패시 ResponseException을 리턴
    def delete_userinfo(self):
        url = self._url + 'userinfo/'
        headers = self.get_header()
        data = {}

        response = self._delete(url, headers=headers, data=data)

        if type(response) == ResponseException:
            return response
        
        self._token = ''
        self._usernum = 0
usersdbinterface = UsersDBInterface()

# 유저 상세정보 관리 인터페이스 클래스
class UserDetailsDBInterface(DBInterface):
    def __init__(self):
        super(UserDetailsDBInterface, self).__init__()
        self._url += 'users/'
        # 성공시 None, 실패시 Popup을 리턴
    # 성공시 None, 실패시 ResponseException을 리턴
    def post_userdetail(self, birth, phone, families, nation, legion, job, jobaddr):
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

        response = self._post(url, headers=headers, data=data)

        if type(response) == ResponseException:
            return response
    # 성공시 유저정보, 실패시 ResponseException을 리턴
    def get_userdetail(self, usernum=None):
        url = self._url + 'userdetail/'
        headers = usersdbinterface.get_header()
        data = {
            'usernum': usernum if usernum else int(headers.get('usernum'))
        }

        response = self._get(url, headers=headers, data=data)

        if type(response) == ResponseException:
            return response
        
        return response
    # 성공시 None, 실패시 ResponseException을 리턴
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
            return response
    # 성공시 None, 실패시 ResponseException을 리턴
    def delete_userdetail(self):
        url = self._url + 'userdetail/'
        headers = usersdbinterface.get_header()
        data = {}

        response = self._put(url, headers=headers, data=data)

        if type(response) == ResponseException:
            return response
userdetaildbinterface = UserDetailsDBInterface()

# 포스트 관리 인터페이스 클래스
class PostsDBInterface(DBInterface):
    def __init__(self):
        super(PostsDBInterface, self).__init__()
        self._url += 'posts/'
        self._id_prefix = ''
    # 성공시 리스트, 실패시 ResponseException을 리턴
    def get_postlist(self, where='', order=''):
        url = self._url + 'postlist/'
        headers = usersdbinterface.get_header()
        data = {
            'id_prefix': self._id_prefix,
            'where': where,
            'order': order
        }

        response = self._get(url, headers=headers, data=data)

        if type(response) == ResponseException:
            if response.code == 404:
                return []
            else:
                return response

        return response.get('id_list')
    # 성공시 {...}, 실패시 ResponseException을 리턴
    def get_post(self, id):
        url = self._url + 'post/'
        headers = usersdbinterface.get_header()
        data = {
            'id': id
        }

        response = self._get(url, headers=headers, data=data)
        if type(response) == ResponseException:
            if response.status_code == 404:
                return {}
            else:
                return response
        
        return response
    # 성공시 None, 실패시 ResponseException을 리턴
    def post_post(self, writedate, content):
        url = self._url + 'post/'
        headers = usersdbinterface.get_header()
        data = {
            'id_prefix': self._id_prefix,
            'writer': headers.get('usernum'),
            'writedate': writedate,
            'content': content
        }

        response = self._post(url, headers=headers, data=data)
        if type(response) == ResponseException:
            return response
    # 현재 id_prefix를 읽음
    def get_id_prefix(self):
        return self._id_prefix
    # 현재 id_prefix를 새로 씀
    def put_id_prefix(self, id_prefix):
        self._id_prefix = id_prefix
postsdbinterface = PostsDBInterface()
