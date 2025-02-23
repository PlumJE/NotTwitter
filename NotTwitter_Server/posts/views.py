from urllib.parse import quote
from django.contrib.auth.models import User
from django.db.models.expressions import RawSQL
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import *

from .models import *


class PostlistView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    # 성공하면 포스트 번호들의 리스트(빈 리스트 포함)을 리턴
    def get(self, request):
        try:
            rawsql = "SELECT posts.id FROM posts_posts AS posts JOIN auth_user AS user ON posts.writer=user.id "

            id_prefix = request.data.get('id_prefix')
            where = request.data.get('where')
            order = request.data.get('order')

            if where:
                rawsql += " WHERE " + where
            elif id_prefix:
                rawsql += " WHERE posts.id regexp '^" + id_prefix + "(/[0-9]+)?$' "
            else:
                rawsql += " WHERE posts.id regexp '^[0-9]+$' "

            if id_prefix:
                rawsql += " ORDER BY posts.id "
            elif not order or order == 'id':
                rawsql += " ORDER BY posts.id DESC "
            else:
                rawsql += " ORDER BY " + order
            # print('rawsql is :', rawsql, 'id_prefix :', id_prefix, 'where :', where, 'order :', order)
            
            posts = [post.id for post in Posts.objects.raw(rawsql)]

            return Response(
                {'id_list': posts},
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

class PostView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    # 포스트에 부여할 새로운 번호를 생성
    def generate_new_id(self, id_prefix):
        new_id_suffix = Posts.objects.filter(id__startswith=id_prefix).count()

        if id_prefix:
            return f"{id_prefix}/{new_id_suffix}"
        return str(new_id_suffix)
    # 성공하면 포스트의 정보를 담은 맵 리턴
    def get(self, request):
        try:
            post_id = request.data.get('id')
            post = Posts.objects.get(id=post_id)

            return Response(
                {
                    'id': post.id,
                    'writer': post.writer,
                    'writedate': post.writedate,
                    'content': post.content
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
    # 성공하면 포스트에게 주어진 번호를 리턴
    def post(self, request):
        try:
            writer = request.data.get('writer')
            writedate = request.data.get('writedate')
            content = request.data.get('content')
            id_prefix = request.data.get('id_prefix')

            new_id = self.generate_new_id(id_prefix)

            Posts.objects.create(
                id=new_id, 
                writer=writer, 
                writedate=writedate, 
                content=content
            )

            return Response(
                {'id': new_id},
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

# 게시글글 이미지 뷰
class PostImgView(APIView):
    # usernum과 이미지를 받아 저장
    def put(self, request):
        try:
            id = request.data.get('id')
            postimg = request.FILES.get('postimg')

            user, created = Posts.objects.update_or_create(
                id=id,
                defaults={'postimg': postimg}
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
    # usernum를 받아 게시글 사진 url을 다운로드
    def get(self, request):
        try:
            id = request.data.get('id')
            post = Posts.objects.get(id=id)

            if post.postimg:
                postimg_url = post.postimg.name
                print('postimg_url is', postimg_url)
                encoded_url = quote(postimg_url, safe=":/")  # 한글 파일명을 URL-safe 하게 변환
            else:
                encoded_url = None

            return Response(
                {'postimg_name': encoded_url},
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
