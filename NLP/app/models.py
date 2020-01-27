from django.db import models

# Create your models here.
class Author(models.Model):
	author_name = models.CharField(max_length=200)
	