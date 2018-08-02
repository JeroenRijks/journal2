# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render, redirect
from journal.models import Resource
from journal.forms import ResourceForm

def home(request):
    resources = Resource.objects.all()
    return render(request, 'home.html', {'name': 'jeroen','items': resources})


def newresource(request, res_id=None):
    print res_id
    if res_id:
        resource = Resource.objects.get(id=res_id)
    else:
        resource=None
    print resource
    if request.POST:
        print request.POST
        if resource:
            form = ResourceForm(data=request.POST, instance=resource)
        else:
            form = ResourceForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('journal:home')
    else:
        if resource:
            form = ResourceForm(instance=resource)
        else:
            form = ResourceForm()
    return render(request, 'form.html', {'form':form, 'name': 'jeroen'})