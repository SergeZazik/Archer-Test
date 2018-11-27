from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from archer_apps.accounts.models import UserTypes

from .models import Article, StatusTypes
from .serializers import ArticleSerializer


class ModeratedArticleList(generics.ListAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        search = self.request.query_params.get('search', None)
        if search is None:
            return Article.objects.filter(status=StatusTypes.REVIEWED.value)
        return Article.objects.filter(status=StatusTypes.REVIEWED.value, title__icontains=search)


class ArticleAPIView(generics.ListCreateAPIView,
                     generics.UpdateAPIView,
                     generics.DestroyAPIView,
                     generics.ListAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    permissions_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        search = self.request.query_params.get('search', None)
        if self.request.user.user_type == UserTypes.EDITOR.value:
            qs = Article.objects.all()
        else:
            qs = Article.objects.filter(creator=self.request.user)
        if search:
            qs = qs.filter(title__icontains=search)
        return qs

    def post(self, request, *args, **kwargs):
        data = request.data.get('data')
        if not data:
            return Response('no field data', status=status.HTTP_400_BAD_REQUEST)
        title = data.get('title')
        content = data.get('content')
        if title is None or content is None:
            return Response('fields title and content is required', status=status.HTTP_400_BAD_REQUEST)
        if request.user.user_type == UserTypes.EDITOR.value:
            moderated = StatusTypes.REVIEWED.value
        else:
            moderated = StatusTypes.UNREVIEWED.value
        article = Article.objects.create(
            title=title,
            content=content,
            status=moderated,
            creator=request.user
        )
        serializer = ArticleSerializer(Article.objects.filter(id=article.id), many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        data = request.data.get('data')
        if not data:
            return Response('no field data', status=status.HTTP_400_BAD_REQUEST)

        article_id = data.get('article_id')
        try:
            article = Article.objects.get(id=article_id)
        except ObjectDoesNotExist:
            return Response('no post with this ID', status=status.HTTP_404_NOT_FOUND)

        if request.user.user_type == UserTypes.EDITOR.value or request.user == article.creator:
            title = data.get('title')
            content = data.get('content')
            if title is None or content is None:
                return Response('fields title and content is required', status=status.HTTP_400_BAD_REQUEST)

            if request.user.user_type == UserTypes.EDITOR.value:
                moderated = StatusTypes.REVIEWED.value
            else:
                moderated = StatusTypes.UNREVIEWED.value

            edited_article = Article.objects.filter(id=article_id).update(
                title=title,
                content=content,
                is_moderated=moderated
            )
            serializer = ArticleSerializer(Article.objects.filter(id=edited_article.id), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response('only Editor or creator can edit or delete post!', status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, *args, **kwargs):
        data = request.data.get("data")
        article_id = data.get('article_id')
        try:
            article = Article.objects.get(id=article_id)
            if request.user == article.creator or request.user.user_type == 'editor':
                article.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response('only Editor or creator can edit or delete post!', status=status.HTTP_403_FORBIDDEN)
        except ObjectDoesNotExist:
            return Response('no post with this ID', status=status.HTTP_404_NOT_FOUND)
