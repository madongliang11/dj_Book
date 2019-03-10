from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from apps.apis import view_set
from rest_framework.documentation import include_docs_urls

router = DefaultRouter()
router.register("art_user", view_set.ArtsUserViewSet)
router.register("tag", view_set.TagViewSet)
router.register("book", view_set.ArtViewSet)
router.register("content", view_set.ContentViewSet)
router.register("chapter", view_set.ChapterViewSet)
router.register("comment", view_set.CommentViewSet)

from apps.apis.view import BookListAPIView

urlpatterns = [
   url(r"^", include(router.urls)),
   url(r"^docs/", include_docs_urls("小说平台api文档")),
   url(r"^api-auth/", include('rest_framework.urls', namespace = "rest_framework")),
   url(r'^recommend/',view_set.ArtViewSet.as_view({'get':'list'}),name='recommend'),
   url(r'^booklist/',BookListAPIView.as_view(),name='recommend')
]
