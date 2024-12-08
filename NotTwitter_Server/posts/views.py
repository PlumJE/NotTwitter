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
            id_prefix = request.data.get('id_prefix', '')
            posts = Posts.objects.filter(id__startswith=id_prefix)
            where = request.data.get('where')
            if where:
                posts = posts.filter(id=RawSQL("SELECT id FROM auth_user WHERE %s", where))
            order = request.data.get('order')
            if order:
                posts = posts.filter(id=RawSQL("SELECT id FROM auth_user WHERE %s ORDER BY %s", where, order))
            
            posts = posts.values_list('id', flat=True)
            if not posts.exists():
                raise NotFound('No posts found with the given prefix')
            
            return Response(
                {'id_list': list(posts)},
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
    def generate_new_id(id_prefix):
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
            id_prefix = request.data.get('id_prefix', '')

            new_id = self.generate_new_id(id_prefix)

            Posts.objects.create(id=new_id, writer=writer, writedate=writedate, content=content)

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
