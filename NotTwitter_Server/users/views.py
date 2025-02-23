from urllib.parse import quote
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import *
from rest_framework.authtoken.models import Token

from .models import *


# 로그인, 로그아웃 뷰
class Loginout(APIView):
    # 로그인 성공시 유저번호 등을 리턴
    def post(self, request):
        try:
            username = request.data.get('nickname')
            email = request.data.get('mailaddr')
            password = request.data.get('password')

            user = authenticate(username=username, password=password)
            if user and user.email == email:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                token_key = token.key
                user_id = user.id
            else:
                token_key = ''
                user_id = 0
                created = False

            return Response(
                {
                    'token': token_key, 
                    'usernum': user_id, 
                    'created': created
                },
                status=status.HTTP_201_CREATED
            )
        except APIException as e:
            return Response(
                {'error': str(e)},
                status=e.status_code
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    # 로그아웃 성공시 메시지를 리턴
    def delete(self, request):
        try:
            user = request.user

            Token.objects.filter(user=user).delete()
            logout(request)

            return Response(
                {'message': 'Logout succeeded'}, 
                status=status.HTTP_200_OK
            )
        except APIException as e:
            return Response(
                {'error': str(e)},
                status=e.status_code
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# 회원가입 및 유저정보 뷰
class UserInfoView(APIView):
    # 회원가입 성공시 메시지를 리턴
    def post(self, request):
        try:
            username = request.data.get('nickname')
            password = request.data.get('password')
            email = request.data.get('mailaddr')

            # 닉네임-이메일-비밀번호 조합이 이미 있으면 거부한다
            user = authenticate(username=username, email=email, password=password)
            if user:
                raise AuthenticationFailed('Invalid username or password!')

            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )

            return Response(
                {'message': 'UserInfos insert succeeded.'},
                status=status.HTTP_201_CREATED
            )
        except APIException as e:
            return Response(
                {'error': str(e)},
                status=e.status_code
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    # 성공시 DB의 회원정보 전부 리턴
    def get(self, request):
        try:
            id = request.data.get('usernum')
            user = User.objects.get(id=id)
            
            return Response(
                {
                    'usernum': user.id,
                    'nickname': user.username,
                    'mailaddr': user.email,
                    'firstname': user.first_name,
                    'lastname': user.last_name,
                    'firstlogin': user.date_joined,
                    'lastlogin': user.last_login
                },
                status=status.HTTP_200_OK
            )
        except APIException as e:
            return Response(
                {'error': str(e)},
                status=e.status_code
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    # 성공시 DB의 회원정보 전부 리턴
    def put(self, request):
        try:
            id = request.headers.get('usernum')
            username = request.data.get('nickname')     # 새롭게 바꿀 닉네임임
            email = request.data.get('mailaddr')
            firstname = request.data.get('firstname')
            lastname = request.data.get('lastname')

            # 닉네임 변경시 이미 있는 닉네임-비밀번호 조합이 발견되면 수정을 거부한다
            user = User.objects.get(id=id)
            if user.username != username and authenticate(username=username, email=email, password=user.password):
                raise AuthenticationFailed('Invalid username or password!')

            user.username=username if username else user.username
            user.email=email if email else user.email
            user.first_name=firstname if firstname else user.first_name
            user.last_name=lastname if lastname else user.last_name
            user.save()

            return Response(
                {
                    'usernum': user.id,
                    'nickname': user.username,
                    'mailaddr': user.email,
                    'firstname': user.first_name,
                    'lastname': user.last_name,
                    'firstlogin': user.date_joined,
                    'lastlogin': user.last_login
                },
                status=status.HTTP_200_OK
            )
        except APIException as e:
            return Response(
                {'error': str(e)},
                status=e.status_code
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    # 성공시 메시지를 리턴
    def delete(self, request):
        try:
            id = request.headers.get('usernum')

            UserDetails.objects.filter(id=id).delete()

            return Response(
                {'message': 'UserInfos delete succeeded.'},
                status=status.HTTP_200_OK
            )
        except APIException as e:
            return Response(
                {'error': str(e)},
                status=e.status_code
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# 유저 상세정보 뷰
class UserDetailView(APIView):
    # 성공시 메세지를 리턴
    def post(self, request):
        try:
            id = request.data.get('usernum')

            UserDetails.objects.create(
                id=id
            )

            return Response(
                {'message': 'UserDetails inserted successfully.'}, 
                status=status.HTTP_201_CREATED
            )
        except APIException as e:
            return Response(
                {'error': str(e)},
                status=e.status_code
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    # 성공시 DB의 상세정보 전부 리턴
    def get(self, request):
        try:
            id = request.data.get('usernum')
            user = UserDetails.objects.get(id=id)
            
            return Response(
                {
                    'usernum': user.id,
                    'birth': user.birth,
                    'phone': user.phone,
                    'families': user.families,
                    'nation': user.nation,
                    'legion': user.legion,
                    'job': user.job,
                    'jobaddr': user.jobaddr
                },
                status=status.HTTP_200_OK
            )
        except APIException as e:
            return Response(
                {'error': str(e)},
                status=e.status_code
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    # 성공시 DB의 상세정보 전부 리턴
    def put(self, request):
        try:
            id = request.headers.get('usernum')

            birth = request.data.get('birth')
            phone = request.data.get('phone')
            families = request.data.get('families')
            nation = request.data.get('nation')
            legion = request.data.get('legion')
            job = request.data.get('job')
            jobaddr = request.data.get('jobaddr')

            user = UserDetails.objects.get(id=id)
            user.birth=birth if birth else user.birth
            user.phone=phone if phone else user.phone
            user.families=families if families else user.families
            user.nation=nation if nation else user.nation
            user.legion=legion if legion else user.legion
            user.job=job if job else user.job
            user.jobaddr=jobaddr if jobaddr else user.jobaddr
            user.save()

            return Response(
                {
                    'usernum': user.id,
                    'birth': user.birth,
                    'phone': user.phone,
                    'families': user.families,
                    'nation': user.nation,
                    'legion': user.legion,
                    'job': user.job,
                    'jobaddr': user.jobaddr
                },
                status=status.HTTP_200_OK
            )
        except APIException as e:
            return Response(
                {'error': str(e)},
                status=e.status_code
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    # 성공시 메시지를 리턴
    def delete(self, request):
        try:
            id = request.headers.get('usernum')

            UserDetails.objects.filter(id=id).delete()

            return Response(
                {'message': 'UserDetails deleted successfully.'},
                status=status.HTTP_200_OK
            )
        except APIException as e:
            return Response(
                {'error': str(e)},
                status=e.status_code
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# 유저 프로필 이미지 뷰
class ProfileImgView(APIView):
    # usernum과 이미지를 받아 저장
    def put(self, request):
        try:
            id = request.data.get('usernum')
            profileimg = request.FILES.get('profileimg')

            user, created = UserDetails.objects.update_or_create(
                id=id,
                defaults={'profileimg': profileimg}
            )

            return Response(
                {'message': '이미지가 저장되었습니다.'},
                status=status.HTTP_200_OK
            )
        except APIException as e:
            return Response(
                {'error': str(e)},
                status=e.status_code
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    # usernum를 받아 프로필 url을 다운로드
    def get(self, request):
        try:
            id = request.data.get('usernum')
            user = UserDetails.objects.get(id=id)

            if user.profileimg:
                profile_url = user.profileimg.name
                encoded_url = quote(profile_url, safe=":/")  # 한글 파일명을 URL-safe 하게 변환
            else:
                encoded_url = 'images/profiles/default.jpeg'  

            return Response(
                {'profile_name': encoded_url},
                status=status.HTTP_200_OK
            )
        except APIException as e:
            return Response(
                {'error': str(e)},
                status=e.status_code
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
