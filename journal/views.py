# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from journal.models import Resource, Tag
from journal.forms import ResourceForm, TagForm


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
    tag_form = TagForm()
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
    return render(request, 'form.html', {'tagform':tag_form, 'form':form, 'name': 'jeroen'})



def deleteresource(request, res_id=None):
    if res_id:
        resource = Resource.objects.get(id=res_id)
    else:
        resource=None
    print res_id
    if request.POST:
        print request.POST
        if resource:
            resource.delete()
    return redirect('journal:home')

def AJAX_tag_create(request):

    tag_name = request.POST.get('tag_name', None)
    if tag_name:
        print(tag_name)
        Tag.objects.create(name=tag_name)
    full_response = {
    "success": True,

    }
    return JsonResponse(data=full_response, safe=False)

