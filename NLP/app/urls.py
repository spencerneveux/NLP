from django.urls import path
from django.views.generic import TemplateView
from . import views
from app.views import IndexView
from app.views import (
    AuthorList,
    AuthorDetailView,
    AuthorCreate,
    AuthorDelete,
    AuthorUpdate,
)
from app.views import (
    ArticleList,
    ArticleDetailView,
    ArticleCreate,
    ArticleUpdate,
    ArticleDelete,
)
from app.views import (
    PublisherArticleList,
    PublisherDetailView,
    PublisherList,
    PublisherCreate,
    PublisherUpdate,
    PublisherDelete,
)
from app.views import KnowledgeList, KnowledgeDetailView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    # Authors
    path("authors/", AuthorList.as_view(), name="author-list"),
    path("author/<int:pk>", AuthorDetailView.as_view(), name="author-detail"),
    path("author/add/", AuthorCreate.as_view(), name="author-add"),
    path("author/<int:pk>/", AuthorUpdate.as_view(), name="author-update"),
    path(
        "author/<int:pk>/delete", AuthorDelete.as_view(), name="author-delete"
    ),
    # Articles
    path("articles/", ArticleList.as_view(), name="article-list"),
    path(
        "article/<int:pk>", ArticleDetailView.as_view(), name="article-detail"
    ),
    path("article/add/", ArticleCreate.as_view(), name="article-add"),
    path("article/<int:pk>", ArticleUpdate.as_view(), name="article-update"),
    path(
        "article/<int:pk>/delete",
        ArticleDelete.as_view(),
        name="article-delete",
    ),
    path("articles/<publisher>/", PublisherArticleList.as_view()),
    # Publishers
    path("publishers/", PublisherList.as_view(), name="publisher-list"),
    path(
        "publisher/<int:pk>",
        PublisherDetailView.as_view(),
        name="publisher-detail",
    ),
    path("publisher/add", PublisherCreate.as_view(), name="publisher-add"),
    path(
        "publisher/<int:pk>",
        PublisherUpdate.as_view(),
        name="publisher-update",
    ),
    path(
        "publisher/<int:pk>/delete",
        PublisherDelete.as_view(),
        name="publisher-delete",
    ),
    # Knowledge
    path("knowledge/", KnowledgeList.as_view(), name="knowledge-list",),
    path(
        "knowledge/<int:pk>",
        KnowledgeDetailView.as_view(),
        name="knowledge-detail",
    ),
]
