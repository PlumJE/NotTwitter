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
    # 로그인을 POST로 실현시킨다.
    def post(self, request):
        try:
            username = request.data.get('nickname')
            password = request.data.get('password')

            user = authenticate(username=username, password=password)
            if not user:
                raise AuthenticationFailed('Nickname-Password combination not found.')

            login(request, user)
            token, created = Token.objects.get_or_create(user=user)

            return Response(
                {
                    'token': token.key, 
                    'usernum': user.id, 
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
    # 로그아웃을 DELETE로 실현시킨다.
    def delete(self, request):
        try:
            user = request.user

            Token.objects.filter(user=user).delete()
            logout(request)

            return Response(
                {'message': 'Logout successful'}, 
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
    # 회원가입
    def post(self, request):
        try:
            username = request.data.get('nickname')
            password = request.data.get('password')
            email = request.data.get('mailaddr')
            firstname = request.data.get('firstname')
            lastname = request.data.get('lastname')

            User.objects.create_user(
                username=username, 
                password=password,
                email=email,
                firstname=firstname,
                lastname=lastname
            )

            return Response(
                {'message': 'Signup successful'}, 
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
    # 회원정보 열람
    def get(self, request):
        try:
            id = request.data.get('usernum')
            userinfo = User.objects.get(id=id)

            username = userinfo.username
            email = userinfo.email
            firstname = userinfo.first_name
            lastname = userinfo.last_name
            firstlogin = userinfo.date_joined
            lastlogin = userinfo.last_login
            
            return Response(
                {
                    'nickname': username,
                    'mailaddr': email,
                    'firstname': firstname,
                    'lastname': lastname,
                    'firstlogin': firstlogin,
                    'lastlogin': lastlogin
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
    # 회원정보 수정
    def put(self, request):
        try:
            id = request.headers.get('usernum')

            username = request.data.get('nickname')
            email = request.data.get('mailaddr')
            firstname = request.data.get('firstname')
            lastname = request.data.get('lastname')

            password = User.objects.filter(id=id).get('password')
            print('password is', password)
            if User.objects.filter(username=username, password=password).exists():
                raise ValidationError('Nickname and password are overlaped.')

            User.objects.filter(id=id).update(
                username=username,
                email=email,
                first_name=firstname,
                last_name=lastname
            )

            # user = request.user
            # user.username = username
            # user.email = email
            # user.first_name = firstname
            # user.last_name = lastname
            # user.save()

            return Response(
                {'message': 'UserInfo updated successfully.'},
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
    # 상세정보 추가
    def post(self, request):
        try:
            id = request.headers.get('usernum')
            # password = User.objects.filter(id=id).get('password')

            birth = request.data.get('birth')
            phone = request.data.get('phone')
            families = request.data.get('families')
            nation = request.data.get('nation')
            legion = request.data.get('legion')
            job = request.data.get('job')
            jobaddr = request.data.get('jobaddr')

            UserDetails.objects.create_user(
                id=id,
                birth=birth,
                phone=phone,
                families=families,
                nation=nation,
                legion=legion,
                job=job,
                jobaddr=jobaddr
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
    # 상세정보 열람
    def get(self, request):
        try:
            id = request.data.get('usernum')
            userdetail = UserDetails.objects.get(id=id)

            birth = userdetail.birth
            phone = userdetail.phone
            families = userdetail.families
            nation = userdetail.nation
            legion = userdetail.legion
            job = userdetail.job
            jobaddr = userdetail.jobaddr
            
            return Response(
                {
                    'birth': birth,
                    'phone': phone,
                    'families': families,
                    'nation': nation,
                    'legion': legion,
                    'job': job,
                    'jobaddr': jobaddr
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
    # 상세정보 수정
    def put(self, request):
        try:
            id = request.headers.get('usernum')
            # password = User.objects.filter(id=id).get('password')

            birth = request.data.get('birth')
            phone = request.data.get('phone')
            families = request.data.get('families')
            nation = request.data.get('nation')
            legion = request.data.get('legion')
            job = request.data.get('job')
            jobaddr = request.data.get('jobaddr')

            UserDetails.objects.filter(id=id).update(
                birth=birth,
                phone=phone,
                families=families,
                nation=nation,
                legion=legion,
                job=job,
                jobaddr=jobaddr
            )

            # user = request.user
            # user.username = username
            # user.email = email
            # user.first_name = firstname
            # user.last_name = lastname
            # user.save()

            return Response(
                {'message': 'UserDetails updated successfully.'},
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
    # 상세정보 삭제
    def delete(self, request):
        try:
            id = request.headers.get('usernum')
            # password = User.objects.filter(id=id).get('password')

            UserDetails.objects.filter(id=id).delete()

            # user = request.user
            # user.username = username
            # user.email = email
            # user.first_name = firstname
            # user.last_name = lastname
            # user.save()

            return Response(
                {'message': 'UserDetails updated successfully.'},
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
