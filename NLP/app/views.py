from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	return HttpResponse("Testing")

def upload(request, id):
	return HttpResponse("Upload Number: %s" % id)

def results(request, id):
	return HttpResponse("Results Number: %s" % id)