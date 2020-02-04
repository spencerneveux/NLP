from django.urls import path
from django.views.generic import TemplateView
from . import views


app_name = 'app'
urlpatterns = [
	path('', views.index, name='index'),
	path('<int:author_id>/', views.upload, name='upload'),
	path('results/', TemplateView.as_view(template_name="about.html")),
]