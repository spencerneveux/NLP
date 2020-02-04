from django.urls import path
from django.views.generic import TemplateView
from . import views
from app.views import AuthorList, AuthorDetailView, AuthorCreate, AuthorDelete, AuthorUpdate
from app.views import ArticleList, ArticleDetailView, ArticleCreate, ArticleUpdate, ArticleDelete
from app.views import PublisherArticleList

urlpatterns = [
	path('authors/', AuthorList.as_view()),
	path('authors/<int:pk>', AuthorDetailView.as_view(), name="author-detail"),
	path('author/add/', AuthorCreate.as_view(), name='author-add'),
	path('author/<int:pk>/', AuthorUpdate.as_view(), name="author-update"),
	path('author/<int:pk>/delete', AuthorDelete.as_view(), name="author-delete"),
	path('articles/', ArticleList.as_view()),
	path('articles/<int:pk>', ArticleDetailView.as_view(), name="article-detail"),
	path('article/add/', ArticleCreate.as_view(), name="article-add"),
	path('article/<int:pk>', ArticleUpdate.as_view(), name="article-update"),
	path('article/<int:pk>/delete', ArticleDelete.as_view(), name="article-delte"),
	path('articles/<publisher>/', PublisherArticleList.as_view()),

]