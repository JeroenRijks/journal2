# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def home(request):
#    return HttpResponse("Hello, world. You're at the journal index.")

    return render(request, 'index.html', {'name': 'jeroen'})

