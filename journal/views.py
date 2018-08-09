# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from journal.models import Resource, Tag
from journal.forms import ResourceForm, TagForm
from journal.serializers import ResourceSerializer, TagSerializer
from rest_framework import generics

def home(request,tag_id=None):

    resources = Resource.objects.all()
    if tag_id:
        resources = resources.filter(tags=tag_id)
        tag = Tag.objects.get(id=tag_id)            #Try Except
    else:
        tag=None
    return render(request, 'home.html', {'name': 'Jeroen','items': resources,'tag':tag})


def newresource(request, res_id=None):
    if res_id:
        try:
            resource = Resource.objects.get(id=res_id)
        except Resource.DoesNotExist:
            resource = None
    else:
        resource = None
    tag_form = TagForm()

    if request.POST:      # This is for the red submit button
        if resource:        # If it exists, edit that instance. Else make a new one.
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
    return render(request, 'form.html', {'tagform':tag_form, 'form':form, 'name': 'Jeroen'})


def deleteresource(request, res_id=None):
    if res_id:
        resource = Resource.objects.get(id=res_id)
    else:
        resource = None
    if request.POST:
        print(request.POST)
        if resource:
            resource.delete()
    return redirect('journal:home')


def AJAX_tag_create(request):
    tag_name = request.POST.get('tag_name', None)
    if tag_name:
        Tag.objects.create(name=tag_name)
    full_response = {
    "success": True,
    }
    return JsonResponse(data=full_response, safe=False)

class TagList(View):

    def get(self, request):
        taginfo = Tag.objects.all()
        return render(request, 'tag_list.html', {'name' : 'Jeroen', 'tags' : taginfo})

    def post(self, request,tag_id=None):    # Only post method on this page is a delete function.
        if tag_id:
            tag=Tag.objects.get(id=tag_id)
            tag.delete()
        return redirect('journal:tag_list') # Got to redirect to the original page, or the button's existence leads to chaos.


class TagEdit(View):
    def get(self, request, tag_id=None):
        if tag_id:     # Used to either give a filled form for editing, or an empty form for creating
            taginfo = Tag.objects.get(id=tag_id)
            form_class = TagForm(instance = taginfo)
        else:
            taginfo=None
            form_class = TagForm()
        return render(request, 'tag_edit.html', {'tag': taginfo, 'tag_form' : form_class})

    def post(self, request, tag_id=None):

        if tag_id:     # Edit or create
            taginfo = Tag.objects.get(id=tag_id)
            form_class = TagForm(request.POST, instance = taginfo)
        else:
            form_class = TagForm(request.POST)

        if form_class.is_valid():
            form_class.save()
        return redirect('journal:tag_list')

class ResourceListCreate(generics.ListCreateAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer


class TagListCreate(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer