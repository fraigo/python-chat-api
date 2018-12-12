from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect


def index(request):
    return HttpResponse(status=403)


def client(request):
    response = redirect('/static/chat/index.html')
    return response
