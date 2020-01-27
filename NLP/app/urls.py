from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('<int:id>/', views.upload, name='upload'),
	path('<int:id>/results', views.results, name='results')
]