from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import *
from rest_framework.authtoken.models import Token


# 로그인, 로그아웃 뷰
class Loginout(APIView):
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
    def put(self, request):
        try:
            id = request.data.get('usernum')
            userinfo = User.objects.get(id=id)

            username = request.data.get('nickname')
            password = userinfo.password
            email = request.data.get('mailaddr')
            firstname = request.data.get('firstname')
            lastname = request.data.get('lastname')

            if User.objects.filter(username=username, password=password).exists():
                raise ValidationError('Nickname and password are overlaped.')

            user = request.user
            user.username = username
            user.email = email
            user.first_name = firstname
            user.last_name = lastname
            user.save()

            return Response(
                {'message': 'Nickname updated successfully.'},
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
