from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Ekyc App Welcome Page")

def not_found(request):
    return HttpResponse("404 not found")