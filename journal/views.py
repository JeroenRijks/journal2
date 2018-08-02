# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render, redirect
from journal.models import Resource
from journal.forms import ResourceForm

def home(request):
#    return HttpResponse("Hello, world. You're at the journal index.")
    resources = Resource.objects.all()
    return render(request, 'home.html', {'name': 'jeroen','items': resources})

def newresource(request):
    if request.POST:
        print request.POST
        form = ResourceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('journal:home')
    else:
        form = ResourceForm()
    return render(request, 'form.html', {'form':form, 'name': 'jeroen'})