from django.urls import path
from . import views

app_name = 'app'
urlpatterns = [
	path('', views.index, name='index'),
	path('<int:author_id>/', views.upload, name='upload'),
	path('/results', views.results, name='results'),
]