# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from journal.models import Resource, Tag
from journal.forms import ResourceForm, TagForm


def home(request):
    resources = Resource.objects.all()
    return render(request, 'home.html', {'name': 'Jeroen','items': resources})


def newresource(request, res_id=None):
    if res_id:
        resource = Resource.objects.get(id=res_id)
        # tags = resource.tags
        # print tags
        # tagtest=Tag.objects.filter(name=resource.tags)
        # print tagtest
    else:
        resource=None
    print res_id, resource
    tag_form = TagForm()

    if request.POST:      # This is for the red submit button
        print "POST"
        print request.POST
        if resource:        # If it exists, edit that instance. Else make a new one.
            print "resource exists"
            form = ResourceForm(data=request.POST, instance=resource)
        else:
            form = ResourceForm(data=request.POST)
        if form.is_valid():
            print "save"
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


# Use a class based view for tags
class TagList(View):
    # form_class = TagForm
    def get(self, request):
        taginfo = Tag.objects.all()
        resources = Resource.objects.all()
        return render(request, 'taglist.html', {'name' : 'Jeroen', 'tags' : taginfo, 'items':resources})


# class TagEditing(View):
#     # form_class = TagForm
#     def get(self, request):
#         taginfo = Tag.objects.all()
#         resources = Resource.objects.all()
#         return render(request, 'taglist.html', {'name': 'Jeroen', 'tags': taginfo, 'items': resources})