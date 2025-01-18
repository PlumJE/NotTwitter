from django.contrib.auth.models import User
from django.db.models.expressions import RawSQL
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import *

from .models import *


class PostlistView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        try:
            rawsql = "SELECT id FROM posts_posts"

            id_prefix = request.data.get('id_prefix')
            where = request.data.get('where')
            order = request.data.get('order')

            if where and order:
                rawsql += " where " + where + " order by " + order
            elif id_prefix:
                rawsql += " where id regexp '^" + id_prefix + "(/[0-9]+)?$' "
            else:
                rawsql += " where id regexp '^[0-9]+$' "

            posts = [post.id for post in Posts.objects.raw(rawsql)]
            if posts == []:
                raise NotFound('No posts found with the given prefix')

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
    def generate_new_id(self, id_prefix):
        new_id_suffix = Posts.objects.filter(id__startswith=id_prefix).count()

        if id_prefix:
            return f"{id_prefix}/{new_id_suffix}"
        return str(new_id_suffix)
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
