from django.conf.urls import url
from django.urls import path, include
from . import views
from .views import (
    IndexView,
    HomeView,
    UserCreate,
    RSSList
)

from .views import (
    KnowledgeList,
    KnowledgeDetailView,
)

from .views import (
    ProfileUpdate
)

from .views import (
    AuthorList,
    AuthorDetailView,
    AuthorCreate,
    AuthorDelete,
    AuthorUpdate,
)
from .views import (
    ArticleList,
    ArticleDetailView,
    ArticleScoreView,
    ArticleCreate,
    ArticleUpdate,
    ArticleDelete,
)
from .views import (
    PublisherArticleList,
    PublisherDetailView,
    PublisherList,
    PublisherCreate,
    PublisherUpdate,
    PublisherDelete,
)

urlpatterns = [

    # ===================
    # Base Views
    # ===================
    path("", IndexView.as_view(), name="index"),
    path("home/", HomeView.as_view(), name="home"),

    # ===================
    # Login
    # ===================
    path('accounts/', include('django.contrib.auth.urls')),

    # ===================
    # Registration
    # ===================
    path("signup", UserCreate.as_view(), name="user-add"),

    # ===================
    # Profile
    # ===================
    path("profile/<int:pk>", ProfileUpdate.as_view(), name="profile"),

    # ===================
    # RSS
    # ===================
    path("rss/", RSSList.as_view(), name="rss-list"),

    # ===================
    # Authors
    # ===================
    path("authors/", AuthorList.as_view(), name="author-list"),
    path("author/<int:pk>", AuthorDetailView.as_view(), name="author-detail"),
    path("author/add/", AuthorCreate.as_view(), name="author-add"),
    path("author/<int:pk>/", AuthorUpdate.as_view(), name="author-update"),
    path(
        "author/<int:pk>/delete", AuthorDelete.as_view(), name="author-delete"
    ),
    
    # ===================
    # Articles
    # ===================
    path("articles/", ArticleList.as_view(), name="article-list"),
    path("article/<int:pk>", ArticleDetailView.as_view(), name="article-detail"),
    path("article/score/<int:pk>", ArticleScoreView.as_view(), name="article-score"),
    path("article/add/", ArticleCreate.as_view(), name="article-add"),
    path("article/<int:pk>", ArticleUpdate.as_view(), name="article-update"),
    path(
        "article/<int:pk>/delete",
        ArticleDelete.as_view(),
        name="article-delete",
    ),
    path("articles/<publisher>/", PublisherArticleList.as_view()),
    
    # ===================
    # Publishers
    # ===================
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
    
    # ===================
    # Knowledge
    # ===================
    path("knowledge/", KnowledgeList.as_view(), name="knowledge-list",),
    path(
        "knowledge/<int:pk>",
        KnowledgeDetailView.as_view(),
        name="knowledge-detail",
    ),

    # ===================
    # Utility
    # ===================
    url(r'^ajax/favorite/$', views.favorite, name='favorite'),
    url(r'^ajax/add_rss/$', views.add_rss_feed, name='add-rss'),
    url(r'^ajax/remove_rss/$', views.remove_rss_feed, name='remove-rss'),
    url(r'^ajax/bookmark/$', views.bookmark, name='bookmark'),
    url(r'^ajax/like/$', views.like, name='like'),
    url(r'^ajax/dislike/$', views.dislike, name='dislike'),
    url(r'^ajax/get_rss_articles/$', views.get_rss_articles, name='get-rss-articles'),
]
