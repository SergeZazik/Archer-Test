from django.urls import path

from .views import ArticleAPIView, ModeratedArticleList

urlpatterns = [
    path('api/articles-list/', ModeratedArticleList.as_view(), name='articles-list'),
    path('api/articles/', ArticleAPIView.as_view(), name='articles'),
]
