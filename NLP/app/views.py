from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from .models import Author, AuthorForm


def index(request):
    authors = Author.objects.order_by('author_name')
    return render(request, "app/index.html", {'authors': authors})


def upload(request, author_id):
    if request.method == 'POST':
        form = AuthorForm(request.POST)

        if form.is_valid():
            return render(request, "app/results.html")

    else:
        form = AuthorForm()

    return render(request, "app/upload.html", {'form': form})


def results(request):
    return render(request, "app/results.html")